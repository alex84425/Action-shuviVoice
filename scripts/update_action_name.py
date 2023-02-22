import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
print(f"folder name: {PROJECT_ROOT.name}")

if "Action-" not in PROJECT_ROOT.name:
    raise ValueError("Wrong repo name, repo should be like 'Action-XXX'")


def get_action_name(root_name):
    # skip "Action-"
    pattern = re.compile("^Action-([A-Z][a-zA-Z0-9]{2,20})$")
    matched = pattern.match(root_name)
    assert matched, "please check action name format"
    return matched.group(1)


action_name = get_action_name(PROJECT_ROOT.name)
print("The new action name is:", action_name)

files = [
    PROJECT_ROOT / "azure-pipelines.yml",
    PROJECT_ROOT / "local.env",
]
for file in files:
    file.write_text(file.read_text().replace("ExecutorTemplate", action_name))
    

files = [    
    PROJECT_ROOT /"integration" / "test_feature.py",    
]
for file in files:
    file.write_text(file.read_text().replace("providertemplate", action_name.lower()))
        


files = [
    PROJECT_ROOT / "pyproject.toml",
    PROJECT_ROOT / "docker-compose.yml",
    PROJECT_ROOT / "docker-compose-debug.yml",
    PROJECT_ROOT / "integration.yml",
]
for file in files:
    file.write_text(file.read_text().replace("executortemplate", action_name.lower()))

PROJECT_ROOT.joinpath("README.md").write_text(f"# Action: {action_name}", encoding="utf-8")
