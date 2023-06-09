![SonarQube Report](https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/actions/workflows/master-sonarqube-report-updater.yml/badge.svg?branch=master)
![Pre-commit Fixer](https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/actions/workflows/daily-pre-commit-fixer.yml/badge.svg?branch=master)
![Pre-commit Updater](https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/actions/workflows/daily-pre-commit-updater.yml/badge.svg?branch=master)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen.svg)](https://github.com/dependabot)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linter: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)

<!-- Pytest Coverage Comment:Begin -->
<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/README.md"><img alt="Coverage" src="https://img.shields.io/badge/Coverage-59%25-orange.svg" /></a><details><summary>Coverage Report </summary><table><tr><th>File</th><th>Stmts</th><th>Miss</th><th>Cover</th><th>Missing</th></tr><tbody><tr><td colspan="5"><b>src/app</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/__init__.py">__init__.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/config.py">config.py</a></td><td>23</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/description.py">description.py</a></td><td>6</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/main.py">main.py</a></td><td>15</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>src/app/action</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/__init__.py">__init__.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py">executor.py</a></td><td>60</td><td>38</td><td>36%</td><td><a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L26-L27">26&ndash;27</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L29-L36">29&ndash;36</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L41-L44">41&ndash;44</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L48-L52">48&ndash;52</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L56-L57">56&ndash;57</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L61">61</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L65-L67">65&ndash;67</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L69">69</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L71-L73">71&ndash;73</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L76">76</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L78">78</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L83">83</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L90-L92">90&ndash;92</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L95-L96">95&ndash;96</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/executor.py#L98">98</a></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/models.py">models.py</a></td><td>18</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py">router.py</a></td><td>62</td><td>34</td><td>45%</td><td><a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L34">34</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L42">42</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L48-L49">48&ndash;49</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L52-L53">52&ndash;53</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L69">69</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L87">87</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L98">98</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L104-L107">104&ndash;107</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L116-L119">116&ndash;119</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L128-L131">128&ndash;131</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L140-L141">140&ndash;141</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L143-L148">143&ndash;148</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L150">150</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L152-L153">152&ndash;153</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/action/router.py#L155-L156">155&ndash;156</a></td></tr><tr><td colspan="5"><b>src/app/debug</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/__init__.py">__init__.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py">router.py</a></td><td>80</td><td>47</td><td>41%</td><td><a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py#L38-L45">38&ndash;45</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py#L50-L55">50&ndash;55</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py#L57-L59">57&ndash;59</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py#L64-L66">64&ndash;66</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py#L68-L72">68&ndash;72</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py#L80-L81">80&ndash;81</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py#L93-L99">93&ndash;99</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py#L101-L103">101&ndash;103</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py#L105-L107">105&ndash;107</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py#L109-L112">109&ndash;112</a>, <a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/debug/router.py#L117-L119">117&ndash;119</a></td></tr><tr><td colspan="5"><b>src/app/health</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/health/__init__.py">__init__.py</a></td><td>0</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/app/health/router.py">router.py</a></td><td>26</td><td>0</td><td>100%</td><td>&nbsp;</td></tr><tr><td colspan="5"><b>src/static</b></td></tr><tr><td>&nbsp; &nbsp;<a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/static/__init__.py">__init__.py</a></td><td>4</td><td>1</td><td>75%</td><td><a href="https://github.com/BPSVCommonService/Action-ExecutorTemplate/blob/undefined/src/static/__init__.py#L7">7</a></td></tr><tr><td><b>TOTAL</b></td><td><b>294</b></td><td><b>120</b></td><td><b>59%</b></td><td>&nbsp;</td></tr></tbody></table></details>

| Tests | Skipped | Failures | Errors | Time |
| ----- | ------- | -------- | -------- | ------------------ |
| 12 | 1 :zzz: | 0 :x: | 0 :fire: | 1.874s :stopwatch: |

<!-- Pytest Coverage Comment:End -->

# How to make a action from the template

## A. Create new repo by template in Github

Open https://github.azc.ext.hp.com/BPSVCommonService/Action-ExecutorTemplate/tree/master and `Use this template`
![image](https://media.github.azc.ext.hp.com/user/14519/files/5de2a1e0-64d9-4d12-9847-9ce5f156c663)
![image](https://media.github.azc.ext.hp.com/user/14519/files/dbfa92a9-41b3-4ca6-aad3-ce414b519dda)

### Allow team members "Maintain"

![setting](https://media.github.azc.ext.hp.com/user/15211/files/bf59ad3f-8861-465c-962c-44ecb851f004)

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

### Dev site Setting:

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

## D. Initialize all branches

```cmd
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

## Git LFS:

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

## Integration Test flowchart (Current)

```mermaid
sequenceDiagram
    Integration Test->>+ATC: Create & Trigger Test Plan
    loop Wait Until Task Done
        Integration Test->>ATC: Get Task Result
        ATC->>-Integration Test: Task Result
    end
    Integration Test->>GitHub: Update GitHub Status
    Integration Test->>ADO: Update ADO Test Point
```

## Integration Test flowchart (Building)

```mermaid
sequenceDiagram
    Integration Test (Part I creation)->>+ATC: Create & Trigger Test Plan
    ATC->>Integration Test (Part I creation): Task ID
    Integration Test (Part I creation)->>ATC: Subscript Task Done
    ATC->>ATC: Wait Until Task Done
    ATC->>ADO: Task Result
    ADO->>Integration Test (Part II verification): Send Task Result To Checker
    Integration Test (Part II verification)->>ADO: Update ADO Test Point
    Integration Test (Part II verification)->>GitHub: Update GitHub Commit Status
```

---

# Related Build URL:

-   [Azure Pipelines](https://dev.azure.com/hp-csrd-validation/vCosmos/_build)
-   [Azure Release](https://dev.azure.com/hp-csrd-validation/vCosmos/_release?_a=releases&view=all&path=%5C)
