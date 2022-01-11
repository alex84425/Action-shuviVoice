# How to use cookiecutter make a action from the template



##  1. Install requirement
* cookiecutter
    * description: A command-line utility that creates projects from cookiecutters (project templates), e.g. creating a Python package project from a Python package project template.
    * install :
    ```
    pip install cookiecutter
    ```
* gh 
    * description: gh is GitHub on the command line. It brings pull requests, issues, and other GitHub concepts to the terminal next to where you are already working with git and your code.
    * install: https://cli.github.com/manual/installation
    
        ```
        # for linux 
        sudo apt update
        sudo apt install gh
        ```
        ```
        # for win10 
        scoop bucket add github-gh https://github.com/cli/scoop-gh.git
        scoop install gh
        # Or
        choco install gh

        ```
    * gh login to set configure:    

        ```
        gh auth login
        # Or authenticate against github.com by reading the token from a file
        gh auth login --with-token < mytoken.txt

        ```
        <img width="551" alt="gh login" src="https://media.github.azc.ext.hp.com/user/25873/files/f1ee01f4-5b45-47a0-b913-6316869c4e75">

 
## 2. Clone template by cookiecutter
```
cookiecutter  git@github.azc.ext.hp.com:BPSVCommonService/Action-ExecutorTemplate.git
```
Notice: cookiecutter currently not support "clone with submodule" and "clone from branch"

## 3. Input required variables
Except input project name, you can keep press "enter" to set in default.

<img width="433" alt="cookie_usertyping" src="https://media.github.azc.ext.hp.com/user/25873/files/eeb8a75b-ebd4-4992-bc2f-fe6b4888c800">

* Expect result

![image](https://media.github.azc.ext.hp.com/user/25873/files/7ba26cbc-2d96-4854-9b5d-2aca6bcfbd56)



<br/><br/>
# Install packeges by poetry
4. Install poetry (python packages dependency manager)
    ```
    cd Action-YourAction
    pip install poetry
    ```

5. if default python version if not 3.8
    ```
    poetry env use C:\Python38\python.exe (your python 3.8 path)
    ```
6. package management  

    - install env
        ```
        poetry install
        ```
    - add module (dev)
        ```
        poetry add -D XXX
        ``` 

    - add module (producetion)
        ```
        poetry add XXX
        ```
        
    - remove module (dev)
        ```
        poetry remove -D XXX
        ```

    - remove module (producetion)
        ```
        poetry remove XXX
        ``` 

<br/><br/>
# Add submodule to your repo


7. add submodule
    - with staic commit
    ```
    git submodule add https://github.azc.ext.hp.com/BPSVCommonService/ActionTemplate-Python3.git
    ```

    - track master
    ```
    git submodule add -b master https://github.azc.ext.hp.com/BPSVCommonService/ActionTemplate-Python3.git
    ```

8. update submodule
```
git submodule update --remote --merge
```

9. clone submodule in a local repo
```
git submodule update --init --recursive
```

10. Remove submodule from your repo
https://gist.github.com/myusuf3/7f645819ded92bda6677

# need to fixs:
1. print("stdout") for subprocess (O)
2. accept null_input("") as default input (O)
3. remove cook url****Alex (O)
4. gh create may ask "Y or N" lead to crush
5. check repo exit before create repo (O)