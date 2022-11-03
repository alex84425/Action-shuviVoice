from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
print(f"folder name: {PROJECT_ROOT.name}")

if "Action-" not in PROJECT_ROOT.name:
    raise ValueError("Wrong repo name, repo should be like 'Action-XXX'")

action_name = PROJECT_ROOT.name.lstrip("Action-")
print("The new action name is:", action_name)

files = [
    PROJECT_ROOT / "src" / "app" / "config.py",
    PROJECT_ROOT / "azure-pipelines.yml",
    PROJECT_ROOT / "integration" / "basicCheckSiteServiceStatusDemo.sh",
]
for file in files:
    file.write_text(file.read_text().replace("ExecutorTemplate", action_name))

files = [
    PROJECT_ROOT / "docker-compose.yml",
    PROJECT_ROOT / "docker-compose-debug.yml",
    PROJECT_ROOT / "pyproject.toml",
    PROJECT_ROOT / "integration" / "test_ping.py",
    PROJECT_ROOT / "integration" / "basicCheckSiteServiceStatusDemo.sh",
    PROJECT_ROOT / "integration.yml",
]
for file in files:
    file.write_text(file.read_text().replace("executortemplate", action_name.lower()))

PROJECT_ROOT.joinpath("README.md").write_text(f"# Action: {action_name}", encoding="utf-8")
