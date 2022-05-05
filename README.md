# How to make a action from the template

## 1. Create new repo by template in Github


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

# Add submodule to your repo

7. init/update submodule
    - execute `update_submodule.bat` or the following command
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
