from pathlib import Path


def test_runtime_has_no_zep_dependencies():
    root = Path(__file__).parents[1]
    forbidden = ("zep_cloud", "ZEP_API_KEY", "services.zep_", "ZepTools", "ZepGraph", "ZepEntity")
    files = list((root / "app").rglob("*.py")) + [root / "requirements.txt", root / "pyproject.toml"]
    violations = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in forbidden):
            violations.append(str(path.relative_to(root)))
    assert not violations, violations
