import re
import sys


MODULE_REGEX = r"^[a-zA-Z]+$"
REMOTE_REGEX = r"git@github\.azc\.ext\.hp\.com:[a-zA-Z]+/[a-zA-Z\-]+\.git"
action_name = "{{cookiecutter.action_name}}"
git_remote = "{{cookiecutter.git_remote}}"


if not re.match(MODULE_REGEX, action_name):
    print(f"ERROR: {action_name}  is not a valid action name, allowed pattern: {MODULE_REGEX}")
    sys.exit(1)


if not re.match(REMOTE_REGEX, git_remote):
    allowed = "git@github.azc.ext.hp.com:YourService/YourAction.git"
    print(f"ERROR: {git_remote}  is not a valid action name, allowed pattern: {allowed}")
    sys.exit(1)
