from app import create_app
from app.models.project import ProjectManager


def test_create_list_and_get_project(tmp_path, monkeypatch):
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    client = create_app().test_client()

    created = client.post("/api/projects", json={
        "name": "FinTrack v2",
        "simulation_requirement": "Evaluate the proposed budgeting experience.",
        "document_text": "A simpler budgeting workflow with automated categories.",
    })
    assert created.status_code == 201
    project = created.get_json()["data"]
    assert project["total_text_length"] > 0

    listed = client.get("/api/projects").get_json()
    assert listed["count"] == 1
    assert listed["data"][0]["project_id"] == project["project_id"]

    fetched = client.get(f"/api/projects/{project['project_id']}")
    assert fetched.status_code == 200
    assert "automated categories" in fetched.get_json()["data"]["document_text"]


def test_project_validation_and_missing_project(tmp_path, monkeypatch):
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    client = create_app().test_client()

    assert client.post("/api/projects", json={}).status_code == 400
    assert client.get("/api/projects/proj_missing").status_code == 404
