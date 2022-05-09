from pathlib import Path

HERE = Path(__file__).parent
print(HERE)
action_name = HERE.name.lstrip("Action-")
print("The new action name is:", action_name)

files = [
    HERE / "docker-compose.yml",
    HERE / "docker-compose-debug.yml",
    HERE / "src" / "app" / "config.py",
    HERE / "azure-pipelines.yml",
]
for file in files:
    file.write_text(file.read_text().replace("ExecutorTemplate", action_name))
