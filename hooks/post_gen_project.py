import re
import sys
import subprocess

MODULE_REGEX = r"^[a-zA-Z]+$"
action_name = "{{cookiecutter.action_name}}"
remote = "{{cookiecutter.git_remote}}"


def git_cmd(cmd: list):
    subprocess.run(["git"] + cmd, capture_output=True, check=True, encoding="utf-8", shell=True)


git_cmd(["init"])
git_cmd(["remote", "add", "origin", remote])
