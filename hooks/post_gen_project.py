import re
import shutil
import sys
import subprocess


ACTION_NAME = "{{cookiecutter.action_name}}"
MODULE_REGEX = r"^[a-zA-Z]+$"
INIT_GIT = "{{cookiecutter.init_git}}"
ADD_GIT_REMOTE = "{{cookiecutter.add_git_remote}}"
GIT_REMOTE_URL = "{{cookiecutter.git_remote_url}}"

GIT_COMMIT = "{{cookiecutter.git_commit}}"
GIT_COMMIT_M = "{{cookiecutter.git_commit_m}}"


def subprocess_cmd(cmd: list):
    cmd = subprocess.list2cmdline((map(str, cmd)))
    # print(cmd)
    print("Try to run: ", cmd)

    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print("ERROR: ", e.output)

    """
    if check:
        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            print("ERROR: ", e.output)
    else:
        p = subprocess.run(cmd, capture_output=True, check=check, shell=True, encoding="utf-8")
        if p.stdout != "":
            print("stdout: ", p.stdout)

        if p.stderr != "":
            print("stderr: ", p.stderr)
    """


if INIT_GIT == "yes" or INIT_GIT == "":
    subprocess_cmd(["git", "init"])

if ADD_GIT_REMOTE == "yes":

    if GIT_REMOTE_URL == "git@github.azc.ext.hp.com:BPSVCommonService/{YourAction}.git":

        print("Notice: Using default remote url", GIT_REMOTE_URL)
        GIT_REMOTE_URL = ("git@github.azc.ext.hp.com:{}/Action-{}.git").format("BPSVCommonService", ACTION_NAME)
    print("GIT_REMOTE_URL:", GIT_REMOTE_URL)

    subprocess_cmd(["git", "remote", "add", "origin", GIT_REMOTE_URL])  # if not exist
    # subprocess_cmd(["remote", "set-url", "origin", GIT_REMOTE_URL], False) if exist


if GIT_COMMIT == "yes" or GIT_COMMIT == "":

    subprocess_cmd(["git", "add", "-A"])

    ask_add_submodule = input(
        " Action-ExecutorTemplate require ActionTemplate-Python3, do you want to add submodule? [yes]"
    )
    if ask_add_submodule == "yes" or ask_add_submodule == "":
        # git submodule add https://github.azc.ext.hp.com/BPSVCommonService/ActionTemplate-Python3.git
        subprocess_cmd(
            ["git", "submodule", "add", "https://github.azc.ext.hp.com/BPSVCommonService/ActionTemplate-Python3.git"]
        )
        subprocess_cmd(["git", "submodule", "update", "--remote", "--merge"])

        subprocess_cmd(["git", "submodule", "update", "--init", "--recursive"])

    else:
        print("skip add submodule ActionTemplate-Python3")

    subprocess_cmd(["git", "commit", "-m", '"' + GIT_COMMIT_M + '"'])

    # create repo
    # gh repo create BPSVCommonService/Action-ATCtest --private
    repo_name = GIT_REMOTE_URL.split(":")[1].split(".")[0]
    add_repo_flag = input("set new repo to [public] of private:")
    while add_repo_flag not in ["public", "private", ""]:
        print("input user para in list: ", ["public", "private", ""])
        add_repo_flag = input("set new repo to [public] of private:")

    if add_repo_flag == "public" or add_repo_flag == "":
        gh_cmd = "gh repo create {} --public".format(repo_name)
    else:
        gh_cmd = "gh repo create {} --private".format(repo_name)
    # check repo exist
    check_repo_exist_cmd = ["git", "ls-remote", GIT_REMOTE_URL]
    check_repo_exist_cmd = subprocess.list2cmdline((map(str, check_repo_exist_cmd)))
    print("Try to cmd:", check_repo_exist_cmd)
    p = subprocess.run(check_repo_exist_cmd, capture_output=True, shell=True, encoding="utf-8")
    # print("err", p.stderr)
    # print( "out",p.stderr)
    if "Repository not found" not in p.stderr:
        print("stderr", p.stderr)
        print("stdout", p.stderr)
        print("ERROR: repo name has been used and other error !!")
        print("Remove repo clone by cookiecutter!")
        shutil.rmtree("Action-{}.git".format(ACTION_NAME))
        sys.exit(1)
    else:
        print("repo name is valid, try to gh create!")

    print("Try to subprocess gh cmd: ", gh_cmd)
    """    
    p = subprocess.run( gh_cmd , capture_output=True, check=True, shell=True,encoding="utf-8")    
    print("Try to run: ", gh_cmd)
    print("stdout: ", p.stdout)
    print("stderr: ", p.stderr)
    """
    try:
        subprocess.check_output(gh_cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print("ERROR: ", e.output)

    subprocess_cmd(["git", "push", "-u", "origin", "master"])
