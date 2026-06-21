"""Prepare and manage OASIS simulations from explicit persona inputs."""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from .oasis_profile_generator import OasisProfileGenerator
from .persona import PersonaInput, dump_personas, load_personas_json
from .simulation_config_generator import SimulationConfigGenerator


class SimulationStatus(str, Enum):
    CREATED = "created"
    PREPARING = "preparing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"
    FAILED = "failed"


class PlatformType(str, Enum):
    TWITTER = "twitter"
    REDDIT = "reddit"


@dataclass
class SimulationState:
    simulation_id: str
    project_id: str
    graph_id: str = ""
    enable_twitter: bool = True
    enable_reddit: bool = True
    status: SimulationStatus = SimulationStatus.CREATED
    entities_count: int = 0
    profiles_count: int = 0
    entity_types: list[str] = field(default_factory=list)
    config_generated: bool = False
    config_reasoning: str = ""
    current_round: int = 0
    twitter_status: str = "not_started"
    reddit_status: str = "not_started"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result = self.__dict__.copy()
        result["status"] = self.status.value
        return result

    def to_simple_dict(self) -> dict[str, Any]:
        return {
            key: self.to_dict()[key]
            for key in (
                "simulation_id", "project_id", "graph_id", "status",
                "entities_count", "profiles_count", "entity_types",
                "config_generated", "error",
            )
        }


class SimulationManager:
    SIMULATION_DATA_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../uploads/simulations")
    )

    def __init__(self):
        os.makedirs(self.SIMULATION_DATA_DIR, exist_ok=True)
        self._simulations: dict[str, SimulationState] = {}

    def _get_simulation_dir(self, simulation_id: str) -> str:
        path = os.path.join(self.SIMULATION_DATA_DIR, simulation_id)
        os.makedirs(path, exist_ok=True)
        return path

    def _save_simulation_state(self, state: SimulationState) -> None:
        state.updated_at = datetime.now().isoformat()
        with open(
            os.path.join(self._get_simulation_dir(state.simulation_id), "state.json"),
            "w", encoding="utf-8"
        ) as handle:
            json.dump(state.to_dict(), handle, ensure_ascii=False, indent=2)
        self._simulations[state.simulation_id] = state

    def _load_simulation_state(self, simulation_id: str) -> SimulationState | None:
        if simulation_id in self._simulations:
            return self._simulations[simulation_id]
        path = os.path.join(self._get_simulation_dir(simulation_id), "state.json")
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        allowed = set(SimulationState.__dataclass_fields__)
        values = {key: value for key, value in data.items() if key in allowed}
        values["simulation_id"] = simulation_id
        values["status"] = SimulationStatus(values.get("status", "created"))
        state = SimulationState(**values)
        self._simulations[simulation_id] = state
        return state

    def create_simulation(
        self,
        project_id: str,
        graph_id: str = "",
        enable_twitter: bool = True,
        enable_reddit: bool = True,
    ) -> SimulationState:
        simulation_id = f"sim_{uuid.uuid4().hex[:12]}"
        state = SimulationState(
            simulation_id=simulation_id,
            project_id=project_id,
            graph_id=graph_id or simulation_id,
            enable_twitter=enable_twitter,
            enable_reddit=enable_reddit,
        )
        self._save_simulation_state(state)
        return state

    def save_personas(
        self, simulation_id: str, personas: list[PersonaInput]
    ) -> str:
        if not personas:
            raise ValueError("at least one persona is required")
        path = os.path.join(self._get_simulation_dir(simulation_id), "personas.json")
        dump_personas(personas, path)
        return path

    def prepare_simulation(
        self,
        simulation_id: str,
        simulation_requirement: str,
        document_text: str,
        defined_entity_types: list[str] | None = None,
        use_llm_for_profiles: bool = True,
        progress_callback: Any = None,
        parallel_profile_count: int = 3,
        personas: list[PersonaInput] | None = None,
    ) -> SimulationState:
        del use_llm_for_profiles, parallel_profile_count
        state = self._load_simulation_state(simulation_id)
        if not state:
            raise ValueError(f"simulation not found: {simulation_id}")
        state.status = SimulationStatus.PREPARING
        state.error = None
        self._save_simulation_state(state)
        try:
            sim_dir = self._get_simulation_dir(simulation_id)
            if personas is None:
                persona_path = os.path.join(sim_dir, "personas.json")
                if not os.path.exists(persona_path):
                    raise ValueError("personas are required before simulation preparation")
                personas = load_personas_json(persona_path)
            if defined_entity_types:
                allowed = set(defined_entity_types)
                personas = [persona for persona in personas if persona.segment in allowed]
            if not personas:
                raise ValueError("no personas matched the requested segments")
            self.save_personas(simulation_id, personas)
            if progress_callback:
                progress_callback("reading", 100, "Personas loaded", current=len(personas), total=len(personas))

            generator = OasisProfileGenerator()
            profiles = generator.generate_profiles_from_personas(personas)
            if state.enable_reddit:
                generator.save_profiles(profiles, os.path.join(sim_dir, "reddit_profiles.json"), "reddit")
            if state.enable_twitter:
                generator.save_profiles(profiles, os.path.join(sim_dir, "twitter_profiles.csv"), "twitter")
            if progress_callback:
                progress_callback("generating_profiles", 100, "Profiles generated", current=len(profiles), total=len(profiles))

            config_generator = SimulationConfigGenerator()
            params = config_generator.generate_config(
                simulation_id=simulation_id,
                project_id=state.project_id,
                graph_id=simulation_id,
                simulation_requirement=simulation_requirement,
                document_text=document_text,
                entities=personas,
                enable_twitter=state.enable_twitter,
                enable_reddit=state.enable_reddit,
            )
            with open(os.path.join(sim_dir, "simulation_config.json"), "w", encoding="utf-8") as handle:
                handle.write(params.to_json())

            state.entities_count = len(personas)
            state.profiles_count = len(profiles)
            state.entity_types = sorted({persona.segment for persona in personas})
            state.config_generated = True
            state.config_reasoning = params.generation_reasoning
            state.status = SimulationStatus.READY
            self._save_simulation_state(state)
            return state
        except Exception as exc:
            state.status = SimulationStatus.FAILED
            state.error = str(exc)
            self._save_simulation_state(state)
            raise

    def get_simulation(self, simulation_id: str) -> SimulationState | None:
        return self._load_simulation_state(simulation_id)

    def list_simulations(self, project_id: str | None = None) -> list[SimulationState]:
        states = []
        for simulation_id in os.listdir(self.SIMULATION_DATA_DIR):
            if simulation_id.startswith("."):
                continue
            state = self._load_simulation_state(simulation_id)
            if state and (project_id is None or state.project_id == project_id):
                states.append(state)
        return states

    def get_profiles(self, simulation_id: str, platform: str = "reddit") -> list[dict[str, Any]]:
        sim_dir = self._get_simulation_dir(simulation_id)
        if platform == "reddit":
            path = os.path.join(sim_dir, "reddit_profiles.json")
            if not os.path.exists(path):
                return []
            with open(path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        path = os.path.join(sim_dir, "twitter_profiles.csv")
        if not os.path.exists(path):
            return []
        import csv
        with open(path, "r", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def get_simulation_config(self, simulation_id: str) -> dict[str, Any] | None:
        path = os.path.join(self._get_simulation_dir(simulation_id), "simulation_config.json")
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def get_run_instructions(self, simulation_id: str) -> dict[str, Any]:
        sim_dir = self._get_simulation_dir(simulation_id)
        config = os.path.join(sim_dir, "simulation_config.json")
        scripts = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scripts"))
        return {
            "simulation_dir": sim_dir,
            "scripts_dir": scripts,
            "config_file": config,
            "commands": {
                platform: f"python {scripts}/run_{platform}_simulation.py --config {config}"
                for platform in ("twitter", "reddit", "parallel")
            },
        }

    def delete_simulation(self, simulation_id: str) -> bool:
        import shutil
        path = os.path.join(self.SIMULATION_DATA_DIR, simulation_id)
        if not os.path.exists(path):
            return False
        shutil.rmtree(path)
        self._simulations.pop(simulation_id, None)
        return True
