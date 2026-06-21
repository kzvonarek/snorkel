"""Report tools backed by Redis AMS and authoritative OASIS artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from .redis_memory import RedisMemoryClient
from .simulation_query import SimulationQueryService
from .simulation_runner import SimulationRunner


@dataclass
class SearchResult:
    facts: list[str]
    edges: list[dict[str, Any]]
    nodes: list[dict[str, Any]]
    query: str
    total_count: int

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()

    def to_text(self) -> str:
        return "\n".join([f"Search: {self.query}", f"Found {self.total_count} results"] + [f"{i}. {fact}" for i, fact in enumerate(self.facts, 1)])


@dataclass
class NodeInfo:
    uuid: str
    name: str
    labels: list[str]
    summary: str
    attributes: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass
class InsightForgeResult:
    query: str
    simulation_requirement: str
    sub_queries: list[str]
    semantic_facts: list[str] = field(default_factory=list)
    entity_insights: list[dict[str, Any]] = field(default_factory=list)
    relationship_chains: list[str] = field(default_factory=list)
    total_facts: int = 0
    total_entities: int = 0
    total_relationships: int = 0

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()

    def to_text(self) -> str:
        lines = [f"## Deep analysis: {self.query}"]
        lines.extend(f"- {fact}" for fact in self.semantic_facts)
        return "\n".join(lines)


@dataclass
class PanoramaResult:
    query: str
    all_nodes: list[NodeInfo] = field(default_factory=list)
    all_edges: list[Any] = field(default_factory=list)
    active_facts: list[str] = field(default_factory=list)
    historical_facts: list[str] = field(default_factory=list)
    total_nodes: int = 0
    total_edges: int = 0
    active_count: int = 0
    historical_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            **self.__dict__,
            "all_nodes": [node.to_dict() for node in self.all_nodes],
            "all_edges": [edge.to_dict() if hasattr(edge, "to_dict") else edge for edge in self.all_edges],
        }

    def to_text(self) -> str:
        lines = [f"## Simulation panorama: {self.query}"]
        lines.extend(f"- {fact}" for fact in self.active_facts)
        return "\n".join(lines)


@dataclass
class AgentInterview:
    agent_name: str
    agent_role: str
    agent_bio: str
    question: str
    response: str
    key_quotes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass
class InterviewResult:
    interview_topic: str
    interview_questions: list[str]
    selected_agents: list[dict[str, Any]] = field(default_factory=list)
    interviews: list[AgentInterview] = field(default_factory=list)
    selection_reasoning: str = ""
    summary: str = ""
    total_agents: int = 0
    interviewed_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "interviews": [item.to_dict() for item in self.interviews]}

    def to_text(self) -> str:
        lines = [f"## Agent interviews: {self.interview_topic}"]
        for item in self.interviews:
            lines.append(f"### {item.agent_name} ({item.agent_role})\n{item.response}")
        if self.summary:
            lines.append(self.summary)
        return "\n\n".join(lines)


class MemoryToolsService:
    def __init__(self, memory_client: RedisMemoryClient | None = None, **_: Any):
        self.memory = memory_client or RedisMemoryClient()

    def search_graph(self, graph_id: str, query: str, limit: int = 10, **_: Any) -> SearchResult:
        return self.quick_search(graph_id, query, limit)

    def quick_search(self, graph_id: str, query: str, limit: int = 10) -> SearchResult:
        hits = self.memory.search(graph_id, query, limit=limit) if self.memory.enabled else []
        facts = [_citation(hit.text, hit.metadata) for hit in hits]
        if not facts:
            exact = SimulationQueryService(graph_id)
            rows = exact.posts(query=query, limit=limit) + exact.comments(query=query, limit=limit)
            facts = [_row_text(row) for row in rows[:limit]]
        return SearchResult(facts=facts, edges=[], nodes=[], query=query, total_count=len(facts))

    def insight_forge(
        self,
        graph_id: str,
        query: str,
        simulation_requirement: str = "",
        report_context: str = "",
        **_: Any,
    ) -> InsightForgeResult:
        sub_queries = [query]
        if simulation_requirement and simulation_requirement != query:
            sub_queries.append(f"{query} in the context of {simulation_requirement}")
        if report_context:
            sub_queries.append(f"evidence for {query} related to {report_context[:200]}")
        facts: list[str] = []
        for sub_query in sub_queries:
            facts.extend(self.quick_search(graph_id, sub_query, limit=8).facts)
        facts = list(dict.fromkeys(facts))
        personas = SimulationQueryService(graph_id).personas()
        return InsightForgeResult(
            query=query,
            simulation_requirement=simulation_requirement,
            sub_queries=sub_queries,
            semantic_facts=facts,
            entity_insights=personas,
            total_facts=len(facts),
            total_entities=len(personas),
        )

    def panorama_search(self, graph_id: str, query: str = "", **_: Any) -> PanoramaResult:
        panorama = SimulationQueryService(graph_id).panorama(query=query or None)
        personas = panorama["personas"]
        nodes = [NodeInfo(
            uuid=str(item.get("identity", index)),
            name=str(item.get("identity", f"Agent {index}")),
            labels=[str(item.get("segment", "Unsegmented"))],
            summary=str(item.get("description", "")),
            attributes=item,
        ) for index, item in enumerate(personas)]
        rows = panorama["posts"] + panorama["comments"]
        facts = [_row_text(row) for row in rows]
        return PanoramaResult(
            query=query,
            all_nodes=nodes,
            active_facts=facts,
            total_nodes=len(nodes),
            total_edges=len(rows),
            active_count=len(facts),
        )

    def get_graph_statistics(self, graph_id: str) -> dict[str, Any]:
        stats = SimulationQueryService(graph_id).statistics()
        return {
            **stats,
            "total_nodes": stats["agents"],
            "total_edges": stats["posts"] + stats["comments"],
            "entity_types": {segment: 1 for segment in stats["segments"]},
        }

    def get_entities_by_type(self, graph_id: str, entity_type: str, **_: Any) -> list[NodeInfo]:
        return [NodeInfo(
            uuid=str(item.get("identity", "")),
            name=str(item.get("identity", "")),
            labels=[str(item.get("segment", "Unsegmented"))],
            summary=str(item.get("description", "")),
            attributes=item,
        ) for item in SimulationQueryService(graph_id).personas() if item.get("segment") == entity_type]

    def get_entity_summary(self, graph_id: str, entity_name: str, **_: Any) -> dict[str, Any]:
        for item in SimulationQueryService(graph_id).personas():
            if item.get("identity") == entity_name:
                return item
        return {}

    def get_simulation_context(self, graph_id: str, simulation_requirement: str = "") -> dict[str, Any]:
        stats = self.get_graph_statistics(graph_id)
        return {
            "simulation_requirement": simulation_requirement,
            "graph_statistics": stats,
            "total_entities": stats["agents"],
            "related_facts": self.quick_search(graph_id, simulation_requirement or "simulation", 10).facts,
        }

    def interview_agents(
        self,
        simulation_id: str,
        interview_requirement: str,
        simulation_requirement: str = "",
        max_agents: int = 5,
        **_: Any,
    ) -> InterviewResult:
        profiles = SimulationQueryService(simulation_id).agents()
        selected = profiles[:max_agents]
        result = InterviewResult(
            interview_topic=interview_requirement,
            interview_questions=[interview_requirement],
            selected_agents=selected,
            selection_reasoning="Selected a deterministic cross-section from the simulation profiles.",
            total_agents=len(profiles),
        )
        if not selected:
            result.summary = "No agent profiles were available."
            return result
        requests = [{"agent_id": int(profile.get("user_id", index)), "prompt": interview_requirement} for index, profile in enumerate(selected)]
        api_result = SimulationRunner.interview_agents_batch(simulation_id, requests, platform=None, timeout=180.0)
        results = (api_result.get("result") or {}).get("results", {}) if api_result.get("success") else {}
        for index, profile in enumerate(selected):
            agent_id = int(profile.get("user_id", index))
            responses = []
            for platform in ("twitter", "reddit"):
                response = results.get(f"{platform}_{agent_id}", {}).get("response")
                if response:
                    responses.append(f"[{platform}] {response}")
            result.interviews.append(AgentInterview(
                agent_name=str(profile.get("name") or profile.get("username") or f"Agent {agent_id}"),
                agent_role=str(profile.get("profession") or "participant"),
                agent_bio=str(profile.get("bio") or profile.get("description") or ""),
                question=interview_requirement,
                response="\n".join(responses) or "No response returned.",
            ))
        result.interviewed_count = len(result.interviews)
        result.summary = f"Interviewed {result.interviewed_count} agents about {interview_requirement}."
        return result


def _citation(text: str, metadata: dict[str, Any]) -> str:
    return f"{text} [source={metadata.get('source', 'AMS')}; platform={metadata.get('platform')}; round={metadata.get('round')}; agent={metadata.get('agent_name')}]"


def _row_text(row: dict[str, Any]) -> str:
    text = next((row.get(key) for key in ("content", "text", "body", "bio") if row.get(key)), json.dumps(row, ensure_ascii=False, default=str))
    identifier = next((row.get(key) for key in ("post_id", "comment_id", "id") if row.get(key) is not None), "unknown")
    return f"{text} [sqlite:{row.get('platform')}:{row.get('source_table')}:{identifier}]"
