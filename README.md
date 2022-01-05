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

    ![image](https://media.github.azc.ext.hp.com/user/14519/files/bf74fa00-6e56-11ec-87dc-cf82db86d731)



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
        
    - remove module (dev)
        ```
        poetry remove -D XXX
        ```

    - remove module (producetion)
        ```
        poetry remove XXX
        ``` 
