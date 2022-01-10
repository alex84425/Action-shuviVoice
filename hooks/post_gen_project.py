import re
import sys
import subprocess
import keyring

ACTION_NAME = "{{cookiecutter.action_name}}"
MODULE_REGEX = r"^[a-zA-Z]+$"
INIT_GIT = "{{cookiecutter.init_git}}"
ADD_GIT_REMOTE = "{{cookiecutter.add_git_remote}}"
GIT_REMOTE_URL = "{{cookiecutter.git_remote_url}}"

GIT_COMMIT = "{{cookiecutter.git_commit}}"
GIT_COMMIT_M = "{{cookiecutter.git_commit_m}}"


def git_cmd(cmd: list,check="True"):
    #subprocess.run(["git"] + cmd, capture_output=True, check=True, encoding="utf-8", shell=True)
    #subprocess.run(["git"] + cmd, capture_output=True, check=True, shell=True)
    #subprocess.run( " ".join(["git"] + cmd), capture_output=True, check=True, shell=True,encoding="utf-8")
    cmd = subprocess.list2cmdline( (  map(str, ["git"] + cmd ) ))
    print(cmd)
    subprocess.run( cmd , capture_output=True, check=check, shell=True,encoding="utf-8")

    """
    process = subprocess.Popen( ["git"] + cmd, stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print( output)
    """



if INIT_GIT == "yes":
    git_cmd(["init"])

if ADD_GIT_REMOTE == "yes":
    #git@github.azc.ext.hp.com:BPSVCommonService/Action-ExecutorTemplateAlex.git
    if GIT_REMOTE_URL =="d":
        print("Notice: Using default url", GIT_REMOTE_URL)
        GIT_REMOTE_URL = ("git@github.azc.ext.hp.com:{}/Action-{}.git").format(
                "BPSVCommonService",
                        ACTION_NAME            )
    print( "GIT_REMOTE_URL:", GIT_REMOTE_URL )
    git_cmd(["remote", "add", "origin", GIT_REMOTE_URL]) #if not exist
    git_cmd(["remote", "set-url", "origin", GIT_REMOTE_URL], False)

if GIT_COMMIT == "yes":

    git_cmd(["add", "-A" ])

    ask_add_submodule = input(" Action-ExecutorTemplate require ActionTemplate-Python3, do you want to add submodule? [yes]")
    if ask_add_submodule == "yes" or  ask_add_submodule == "":
        #git submodule add https://github.azc.ext.hp.com/BPSVCommonService/ActionTemplate-Python3.git
        git_cmd(["submodule", "add", "https://github.azc.ext.hp.com/BPSVCommonService/ActionTemplate-Python3.git"])

    else:
        print("skip add submodule ActionTemplate-Python3")
    


    git_cmd(["commit", "-m", "\"" + GIT_COMMIT_M + "\""  ])
    
    repo_name = GIT_REMOTE_URL.split(":")[1].split(".")[0]

    # create repo
    #gh repo create BPSVCommonService/Action-ATCtest --private
    add_repo_flag = input("set new repo to [public] of private:")
    if add_repo_flag == "public" or  add_repo_flag == "":
        gh_cmd = "gh repo create {} --public".format(repo_name)
    else:
        
        gh_cmd = "gh repo create {} --private".format(repo_name)    
    print("gh_cmd:",gh_cmd)
    subprocess.run( gh_cmd , capture_output=True, check=True, shell=True,encoding="utf-8")

    """
    setting gh configure
    """
    git_cmd(["push","-u","origin","master"])

  
    
