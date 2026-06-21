"""Project CRUD endpoints used by the demo workflow."""

from flask import jsonify, request

from . import projects_bp
from ..models.project import ProjectManager
from ..utils.logger import get_logger


logger = get_logger("mirofish.api.projects")


@projects_bp.route("", methods=["POST"])
def create_project():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name") or "").strip()
    requirement = str(data.get("simulation_requirement") or "").strip()
    document_text = str(data.get("document_text") or "").strip()

    if not name:
        return jsonify({"success": False, "error": "Project name is required"}), 400
    if not requirement:
        return jsonify({"success": False, "error": "Simulation requirement is required"}), 400

    try:
        project = ProjectManager.create_project(name=name)
        project.simulation_requirement = requirement
        project.total_text_length = len(document_text)
        ProjectManager.save_extracted_text(project.project_id, document_text)
        ProjectManager.save_project(project)
        return jsonify({"success": True, "data": project.to_dict()}), 201
    except Exception as exc:
        logger.exception("Failed to create project")
        return jsonify({"success": False, "error": str(exc)}), 500


@projects_bp.route("", methods=["GET"])
def list_projects():
    limit = max(1, min(request.args.get("limit", 50, type=int), 100))
    projects = ProjectManager.list_projects(limit=limit)
    return jsonify({
        "success": True,
        "data": [project.to_dict() for project in projects],
        "count": len(projects),
    })


@projects_bp.route("/<project_id>", methods=["GET"])
def get_project(project_id: str):
    project = ProjectManager.get_project(project_id)
    if not project:
        return jsonify({"success": False, "error": f"Project not found: {project_id}"}), 404
    payload = project.to_dict()
    payload["document_text"] = ProjectManager.get_extracted_text(project_id) or ""
    return jsonify({"success": True, "data": payload})
