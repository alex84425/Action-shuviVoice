# How to make a action from the template

## 1. Create new repo by template in Github

![image](https://media.github.azc.ext.hp.com/user/14519/files/5de2a1e0-64d9-4d12-9847-9ce5f156c663)
![image](https://media.github.azc.ext.hp.com/user/14519/files/9e6272da-97ee-4619-911c-8839d9b9b663)

<br/><br/>

# Install packeges by poetry

4. Install poetry (python packages dependency manager)

    ```
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

    - add/update module to specific version (producetion)
        ```
        poetry add XXX==version
        ```

    - remove module (dev)
        ```
        poetry remove -D XXX
        ```

    - remove module (producetion)
        ```
        poetry remove XXX
        ```

7. Git LFS
    - lfs track a new file type
        ```
        git lfs track *.zip
        ```

    - check file was tracked by lfs
        ```
        git lfs ls-files
        ```

<br/><br/>

# Clone or update submodule to your repo

7. init/update submodule
    - execute `update_submodule.cmd` or the following command
    ```
    git submodule update --init --recursive --remote 
    ```

10. Remove submodule from your repo
    https://gist.github.com/myusuf3/7f645819ded92bda6677

# Related URL

-   Jenkins

```
https://boss.corp.hpicloud.net/job/BPSValidation/job/BPSVCommonService/
```

# need to fixs:

1. print("stdout") for subprocess (O)
2. accept null_input("") as default input (O)
3. remove cook url\*\*\*\*Alex (O)
4. gh create may ask "Y or N" lead to crush
5. check repo exit before create repo (O)
