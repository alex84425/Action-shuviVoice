import re
import sys
import subprocess
import keyring


MODULE_REGEX = r"^[a-zA-Z]+$"
INIT_GIT = "{{cookiecutter.init_git}}"
ADD_GIT_REMOTE = "{{cookiecutter.add_git_remote}}"
GIT_REMOTE_URL = "{{cookiecutter.git_remote_url}}"


def git_cmd(cmd: list):
    #subprocess.run(["git"] + cmd, capture_output=True, check=True, encoding="utf-8", shell=True)
    process = subprocess.Popen(["git", "init"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print( output)



if INIT_GIT == "yes":
    oubprocess.run(["git"] + cmd, capture_output=True, check=True, encoding="utf-8", shell=True)
    git_cmd(["init"])

if ADD_GIT_REMOTE == "yes":
    git_cmd(["remote", "add", "origin", GIT_REMOTE_URL])
