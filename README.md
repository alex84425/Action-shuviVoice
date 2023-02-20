<!-- Pytest Coverage Comment:Begin -->
<a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/README.md"><img alt="Coverage" src="https://img.shields.io/badge/Coverage-22%25-red.svg" /></a><details><summary>Coverage Report </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td colspan="5"><b>src/tests</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/__init__.py">__init__.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/conftest.py">conftest.py</a></td><td>35</td><td>27</td><td>22%</td><td><a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/conftest.py#L10">10</a>, <a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/conftest.py#L12">12</a>, <a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/conftest.py#L14-L15">14&ndash;15</a>, <a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/conftest.py#L18-L21">18&ndash;21</a>, <a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/conftest.py#L24-L27">24&ndash;27</a>, <a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/conftest.py#L30-L32">30&ndash;32</a>, <a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/conftest.py#L35-L38">35&ndash;38</a>, <a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/conftest.py#L41-L42">41&ndash;42</a>, <a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/conftest.py#L45">45</a>, <a href="https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/blob/2bb528ff40ed312d029e5829cc306b2c68d15f40/src/tests/conftest.py#L50-L54">50&ndash;54</a></td></tr><tr><td><b>TOTAL</b></td><td><b>35</b></td><td><b>27</b></td><td><b>22%</b></td><td>&nbsp;</td></tr></tbody></table></details>

| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 1 | 0 :zzz: | 0 :x: | 1 :fire: | 0.533s :stopwatch: |

<!-- Pytest Coverage Comment:End -->

# How to make a action from the template

## A. Create new repo by template in Github

Open https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/tree/master and `Use this template`
![image](https://media.github.azc.ext.hp.com/user/14519/files/5de2a1e0-64d9-4d12-9847-9ce5f156c663)
![image](https://media.github.azc.ext.hp.com/user/14519/files/dbfa92a9-41b3-4ca6-aad3-ce414b519dda)

## B. Initialize this repository

1. Execute following commands and it will sync the upstream and update action name

> You may need to setup [PAT] for submodules download

[pat]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

```cmd
echo "Clone template"
git clone --recurse-submodules git@github.azc.ext.hp.com:BPSVCommonService/Action-MyTestAction.git
cd Action-MyTestAction

echo "Sync up template"
.\scripts\update_template.cmd

echo "Update action name"
py update_action_name.py
git add .
git commit -m 'rename action'
git push

echo "Initialize all branches"
git checkout -b itg
git push -f -u origin itg
git checkout -b prd
git push -f -u origin prd
git checkout -b dev
git push -f -u origin dev
git checkout master

echo "ALL DONE"
```

Try to run the container `docker compose up` and open browser `http://localhost:8080`

## C. Add Azure Pipeline

1. ⛔ Please make sure `.\scripts\local_build.cmd` pass before add Azure Pipeline

<!--
<img src='https://media.github.azc.ext.hp.com/user/15211/files/e83de2b7-a3c3-47c5-a386-86de2d133d2f' align='top'/> -->

2. <img src='https://media.github.azc.ext.hp.com/user/14519/files/1253a1ca-7d6a-48c5-af55-25f550b50dd1' align='top'/>
3. <img src='https://media.github.azc.ext.hp.com/user/14519/files/663b5d63-b7ff-4509-a5bf-3bc385e02659' align='top'/>
4. <img src='https://media.github.azc.ext.hp.com/user/14519/files/3aa4cc49-ec13-45f2-a4a0-03d7a4235bdf' align='top'/>
5. <img src='https://media.github.azc.ext.hp.com/user/14519/files/553e954d-0e8a-4916-a995-be3c2f1e24e2' align='top'/>

> The newly created repo may take a while to appear

6. <img src='https://media.github.azc.ext.hp.com/user/14519/files/e3628d33-cc54-4241-8c54-f141b936452a' align='top'/>
7. <img src='https://media.github.azc.ext.hp.com/user/14519/files/00687dd3-bf3f-4bc3-a1c5-b143fe80cf57' align='top'/>
8. <img src='https://media.github.azc.ext.hp.com/user/14519/files/7d8714de-afcd-46c0-9582-cd0a716e6aec' align='top'/>

<!--
## D. Add Azure Release

9. <img src='https://media.github.azc.ext.hp.com/user/14519/files/6c9483b7-a109-4c1a-a68c-360947538873' align='top'/>

### Dev site Setting

10. <img src='https://media.github.azc.ext.hp.com/user/15211/files/48a499d1-7c47-497d-990a-c9714aafc5ed' align='top'/>
11. <img src='https://media.github.azc.ext.hp.com/user/14519/files/6d81ff33-d773-470b-98fd-33a4624873a1' align='top'/>
12. <img src='https://media.github.azc.ext.hp.com/user/14519/files/0c0162d5-097f-4860-bb68-8e769b964c25' align='top'/>
13. <img src='https://media.github.azc.ext.hp.com/user/14519/files/2b4741e3-e040-4926-af38-1a85ed29c810' align='top'/>
14. <img src='https://media.github.azc.ext.hp.com/user/14519/files/26b1ca7e-1fd7-4c95-9f3e-4a954b3cafc7' align='top'/>
15. <img src='https://media.github.azc.ext.hp.com/user/14519/files/26e3b051-28d1-4467-b9f4-d0a5035be1ef' align='top'/>
16. <img src='https://media.github.azc.ext.hp.com/user/14519/files/e93a8acc-2ad0-41f9-8bbb-0c507ebe95f9' align='top'/>

### Qa/Itg/Prd Site Setting

Please follow the same steps 10 ~ 12 of `Dev site Setting` (branch in step 12 should be selected to master/itg/prd)

**IMPORTANT** 13~16 only for Dev site
-->

---

# Features

## APIs

-   Console Log https://vcosmos-tpe-qa-1.corp.hpicloud.net/action-executortemplate/log
-   Task Log https://vcosmos-tpe-qa-1.corp.hpicloud.net/action-executortemplate/taskid/{taskid}
    (ex: https://vcosmos-tpe-itg-3.corp.hpicloud.net/action-executortemplate/taskid/c7463_00)
-   Commit id https://vcosmos-tpe-qa-1.corp.hpicloud.net/action-executortemplate/action/info
-   Version and History https://vcosmos-tpe-qa-1.corp.hpicloud.net/action-executortemplate

## Log analysis

![image](https://media.github.azc.ext.hp.com/user/14519/files/a075bd6c-6708-40fb-a9ff-dfe76ec61aaa)

-   Task Id: XXXXX_YY
    -   XXXXX: last five character of atc task id
    -   YY: The order of target actions, from 00 to 99
-   Request Id: A random id for per request

# Development tools tutorial

## [Poetry]: a tool for dependency management and packaging in Python.

[poetry]: https://python-poetry.org/docs/basic-usage/

-   Install poetry `pip install poetry`
-   List your all python version and its path `py -0p`
-   Select python version 3.9 for this project

    `poetry env use C:\Python39\python.exe (your python 3.9 path)`

-   Activate virtual env `poetry shell`
-   Install dependency `poetry install`
-   Examples of adding dependencies package
    -   Add package `httpx` to producetion `poetry add httpx@latest`
    -   Add package `pytest` to development `poetry add -D pytest@latest`
-   Examples of adding dependencies package
    -   Remove package `httpx` from producetion `poetry remove httpx`
    -   Remove package `pytest` from development `poetry remove -D pytest`
-   Examples of dependencies package version control
    -   Lock in specific version `poetry add httpx==0.22.0`
    -   Allow specific version or newer `poetry add httpx>=0.22.0`

## Git Tools - [Submodules]:

[submodules]: https://git-scm.com/book/en/v2/Git-Tools-Submodules

-   After clone this repo, you should also pull the submodules. We provide a command file for init & update submodules.

    Simply run `update_submodule.cmd` and it will help to do the following command _`git submodule update --init --recursive --remote`_

-   [Remove] submodule `git rm <path-to-submodule>` and commit.

[remove]: https://gist.github.com/myusuf3/7f645819ded92bda6677

## Git LFS

-   lfs track a new file type `git lfs track *.zip`
-   check file was tracked by lfs `git lfs ls-files`

## pre-commit

-   Install: poetry run pre-commit install
-   Manual Run: poetry run pre-commit run --all-files

## In the future, if you want to sync up template again, you can run the command

```cmd
echo "Sync up template"
git remote add upstream git@github.azc.ext.hp.com:BPSVCommonService/Action-ExecutorTemplate.git
git fetch upstream
git merge upstream/master --allow-unrelated-histories
git remote remove upstream
```

## How to remove a service?

1.  Add `disable_nginx_location: true` in `azure-pipelines.yml` and deploy once
2.  Go to site portainer, Example [dev-portainer]
3.  Remove Container & image

[dev-portainer]: https://vcosmos-tpe-itg-3.corp.hpicloud.net/portainer/#!/home

---

# Related Build URL

-   [Azure Pipelines](https://dev.azure.com/hp-csrd-validation/vCosmos/_build)
-   [Azure Release](https://dev.azure.com/hp-csrd-validation/vCosmos/_release?_a=releases&view=all&path=%5C)
