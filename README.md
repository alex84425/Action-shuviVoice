# How to use cookiecutter make a action from the template
1. Install cookiecutter

    ```
    pip install cookiecutter
    ```

2. clone repo by cookiecutter
    ```
    cookiecutter git@github.azc.ext.hp.com:BPSVCommonService/Action-ExecutorTemplate.git
    ```

3. Input required variables
    ![image](https://media.github.azc.ext.hp.com/user/14519/files/50a0ab00-6f01-11ec-97b0-1d322ce2dfce)
    ![image](https://media.github.azc.ext.hp.com/user/14519/files/70d06a00-6f01-11ec-9ad0-d845831fc764)


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
