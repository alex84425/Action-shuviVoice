import re
import sys


MODULE_REGEX = r"^[a-zA-Z]+$"
REMOTE_REGEX = r"git@github\.azc\.ext\.hp\.com:[a-zA-Z]+/[a-zA-Z\-]+\.git"
ACTION_NAME = "{{cookiecutter.action_name}}"
INIT_GIT = "{{cookiecutter.init_git}}"
ADD_GIT_REMOTE = "{{cookiecutter.add_git_remote}}"
GIT_REMOTE_URL = "{{cookiecutter.git_remote_url}}"

GIT_COMMIT = "{{cookiecutter.git_commit}}"
GIT_COMMIT_M = "{{cookiecutter.git_commit_m}}"

YES_NO = ["yes","YES", "no","NO"]

if INIT_GIT not in YES_NO:
    print(f"ERROR: init_git  the value should be {YES_NO}")
    sys.exit(1)

if INIT_GIT not in YES_NO:
    print(f"ERROR: add_git_remote  the value should be {YES_NO}")
    sys.exit(1)


if not re.match(MODULE_REGEX, ACTION_NAME):
    print(f"ERROR: {ACTION_NAME}  is not a valid action name, allowed pattern: {MODULE_REGEX}")
    sys.exit(1)


if GIT_REMOTE_URL == "git@github.azc.ext.hp.com:YourService/YourAction.git" :
    print("ERROR: please input your git_remote_url")
    sys.exit(1)




if ADD_GIT_REMOTE == YES_NO[0:2] and not re.match(REMOTE_REGEX, GIT_REMOTE_URL):
    allowed = "git@github.azc.ext.hp.com:YourService/YourAction.git or d(default)"

    
    print(f"ERROR: {GIT_REMOTE_URL}  is not a valid action name, allowed pattern: {allowed}")
    sys.exit(1)

if GIT_COMMIT not in  YES_NO:
    print(f"ERROR: git commit  the value should be {YES_NO}")
    sys.exit(1)

if GIT_COMMIT_M == "" and GIT_COMMIT ==  YES_NO[0:2]:
    print(f"ERROR: git commit  the value should be {YES_NO}")
    sys.exit(1)

