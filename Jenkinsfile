String CRON_SETTINGS = BRANCH_NAME == "master" ? '0 8 * * *' : ""

pipeline {
    agent {
        label 'rndit'
    }

    triggers {
        cron(CRON_SETTINGS)
    }

    options {
        timestamps();
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        office_365_webhook_general_id = '0ce6cd48-b0d4-45ed-a279-0d49f5332dc5'
        office_365_webhook_release_id = '1d3cff49-af7a-452f-8191-3653598a61ec'
        AWS_DEFAULT_REGION            = 'ap-southeast-1'
        category_name                 = 'codedeploy/package'
        service_name                  = 'site/action/executor-template'
        project_name                  = 'action-executor-template'

        docker_user                   = 'theohuang'
        docker_pass                   = '656c88e8-64f1-4f30-a2f2-d43b169e6775'
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    job_name           = env.JOB_NAME.replace(' ', '-')
                    session_scm        = checkout(scm)
                    session_scm_url    = session_scm.GIT_URL[0..-5]+'/commit/'+session_scm.GIT_COMMIT
                    session_docker_url = job_name.split('/')[2].toLowerCase()+':'+session_scm.GIT_BRANCH.replace('/', '-')
                    session_name       = job_name.replace('%2F', '/').replace('/', '-')+'-'+env.BUILD_ID
                    session_tag        = sh(returnStdout: true, script: "git describe --tags --exact-match $session_scm.GIT_COMMIT || true").trim()

                    docker_name        = project_name.toLowerCase().replace('/', '-')
                    container_name     = docker_name+"-"+session_scm.GIT_BRANCH.toLowerCase().replace('/', '-')+"-"+env.BUILD_ID.toLowerCase()
                    container_network  = container_name.toLowerCase()+'-net'

                    prod_docker_base   = docker_name
                    prod_docker_tag    = session_scm.GIT_BRANCH.replace('/', '-')
                    prod_docker        = prod_docker_base+':'+prod_docker_tag

                    aws_access_id = ''
                    if (session_scm.GIT_BRANCH == 'prd') {
                        print('Production')
                        aws_access_id = 'b3ce7628-a1cd-4c13-8c85-2fb87b465790'
                    } else if (session_scm.GIT_BRANCH == 'itg') {
                        print('Integration')
                        aws_access_id = '55867ff1-d927-4001-8582-b862cd8fcbee'
                    } else if (session_scm.GIT_BRANCH == 'master') {
                        print('QA')
                        aws_access_id = '2e18909b-be7d-434a-ad40-f55cd5a63b3b'
                    }
                }
                teamsNotify(1, '')
            }
        }
        stage('Build Dev Image') {
            steps {
                sh "docker login -u ${docker_user} -p ${docker_pass}"
                sh "docker build --pull --target=dev-base --network=host -t ${docker_name}:dev-base . "
            }
        }
        stage('Linter') {
            steps {
                sh "docker build --pull --target=dev-linter --network=host -t ${docker_name}:dev-linter . "
            }
        }
        stage('Utest Coverage') {
            steps {
                sh "docker build --pull --target=dev-coverage --network=host -t ${docker_name}:dev-coverage . "
                sh """
                    docker create --name=${container_name} ${docker_name}:dev-coverage
                    docker cp ${container_name}:/var/src/htmlcov/ htmlcov/
                    docker cp ${container_name}:/var/src/coverage.xml coverage.xml
                    ls -al
                    docker rm -v ${container_name}
                """
                archiveArtifacts(
                    artifacts: "htmlcov/",
                    onlyIfSuccessful: true
                )
                cobertura(
                    coberturaReportFile: "coverage.xml",
                    onlyStable: false,
                    failNoReports: true,
                    failUnhealthy: false,
                    failUnstable: false,
                    autoUpdateHealth: true,
                    autoUpdateStability: false,
                    zoomCoverageChart: true,
                    maxNumberOfBuilds: 0,
                    lineCoverageTargets: '30, 0, 0',
                    conditionalCoverageTargets: '0, 0, 0',
                    methodCoverageTargets: '30, 0, 0'
                )
            }
        }
        stage('Security Check') {
            steps {
                sh "docker build --pull --target=dev-security --network=host -t ${docker_name}:dev-security . "
            }
        }
        stage('Build Prod Image') {
            when { expression { return aws_access_id } }
            steps {
                script {
                    sh "docker build --network=host -t $docker_name . "
                    sh "docker build --network=host -t $prod_docker . "
                }
            }
        }
    }
    post {
        success {
            teamsNotify(2, '')
            script {
                if (
                    session_scm.GIT_BRANCH == 'prd'
                    || session_scm.GIT_BRANCH == 'itg'
                    || session_scm.GIT_BRANCH == 'master'
                ) {
                    teamsNotify(0, '')
                }
            }
        }
        failure {
            teamsNotify(3, '')
        }
        always {
            cleanWs()
            sh "docker logout"
        }
    }
}

def teamsNotify(Integer stage, String message) {
    withCredentials([
        string(
            credentialsId: office_365_webhook_general_id,
            variable: 'office_365_webhook_general',
        ),
        string(
            credentialsId: office_365_webhook_release_id,
            variable: 'office_365_webhook_release',
        ),
    ]) {
        switch(stage) {
            case 0:
                office365ConnectorSend(
                    message: "<table style=\"width:100%\"><tr><th>Release</th><td>$project_name</td></tr><tr><th>GitHub</th><td><$session_scm_url></td></tr></table><br />$message",
                    webhookUrl: office_365_webhook_release,
                    status: 'SUCCESS',
                    color: '05d222',
                )
            break
            case 1:
                office365ConnectorSend(
                    message: "<table style=\"width:100%\"><tr><th>Start build</th><td>$project_name</td></tr><tr><th>Current build</th><td>$session_name</td></tr><tr><th>GitHub</th><td><$session_scm_url></td></tr></table><br />$message",
                    webhookUrl: office_365_webhook_general,
                )
            break
            case 2:
                office365ConnectorSend(
                    message: "<table style=\"width:100%\"><tr><th>Build success</th><td>$project_name</td></tr><tr><th>Current build</th><td>$session_name</td></tr><tr><th>GitHub</th><td><$session_scm_url></td></tr></table><br />$message",
                    webhookUrl: office_365_webhook_general,
                    status: 'SUCCESS',
                    color: '05d222',
                )
            break
            case 3:
                office365ConnectorSend(
                    message: "<table style=\"width:100%\"><tr><th>Build failed</th><td>$project_name</td></tr><tr><th>Current build</th><td>$session_name</td></tr><tr><th>GitHub</th><td><$session_scm_url></td></tr></table><br />$message",
                    webhookUrl: office_365_webhook_general,
                    status: 'FAILED',
                    color: 'd00000',
                )
            break
        }
    }
}
