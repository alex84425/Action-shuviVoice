from pathlib import Path

HERE = Path(__file__).parent.resolve()
print(f"folder name: {HERE.name}")

if "Action-" not in HERE.name:
    raise ValueError("Wrong repo name, repo should be like 'Action-XXX'")

action_name = HERE.name.lstrip("Action-")
print("The new action name is:", action_name)

files = [
    HERE / "src" / "app" / "config.py",
    HERE / "azure-pipelines.yml",
]
for file in files:
    file.write_text(file.read_text().replace("ExecutorTemplate", action_name))

files = [
    HERE / "docker-compose.yml",
    HERE / "docker-compose-debug.yml",
]
for file in files:
    file.write_text(file.read_text().replace("executortemplate", action_name.lower()))

HERE.joinpath("README.md").write_text(f"# Action: {action_name}")