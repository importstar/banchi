def remote=[:]
remote.name = 'binhla'
remote.host = 'binhla2.importstar.dev'
remote.allowAnyHosts = true

pipeline {
    // agent any
    agent {
        docker {
            image 'python:3.12'
        }
    }
    environment {
        BINHLA_CREDS=credentials('binhla2')          
        DOCKER_CREDENTIALS = credentials('c0429270-c4a9-4ce7-a71b-63f1ae62652f')
        WEB_IMAGE_NAME = 'banchi-image'      
        IMAGE_TAG = 'latest'                        
        PROJECT_NAME = 'banchi'              
        PRODUCTION_SERVER = 'binhla2.importstar.dev'   
        GIT_REPO_URL = 'https://github.com/importstar/banchi.git'
        GIT_BRANCH = 'main'
        DOCKER_COMPOSE_PATH = '/home/projects/banchi/docker-compose-production.yml' 
        PROJECT_PATH = '/home/projects/banchi'
        BO_BUILD_PATH = '.' 
        POETRY_HOME = "/root/.poetry/bin"     
        PATH = "$POETRY_HOME:$PATH"
        JAVA_HOME = "/usr/lib/jvm/java-17-openjdk-amd64"
    }

    stages {
        stage('Setup System (Install Java, NPM and Python)') {
            steps {
                sh '''
                echo "Updating package list and installing npm and python..."
                apt-get update && apt-get install -y nodejs npm pip openjdk-17-jdk

                echo "Setting up JAVA_HOME..."
                export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
                echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> ~/.profile
                echo "export PATH=$JAVA_HOME/bin:$PATH" >> ~/.profile
                . ~/.profile

                java -version || exit 1

                echo "Installing Poetry..."
                curl -sSL https://install.python-poetry.org | python3 -

                if [ -f "/root/.poetry/bin/poetry" ]; then
                    export POETRY_HOME="/root/.poetry/bin"
                elif [ -f "/root/.poetry/bin/bin/poetry" ]; then
                    export POETRY_HOME="/root/.poetry/bin/bin"
                else
                    echo "Poetry installation failed."
                    exit 1
                fi

                echo "export POETRY_HOME=$POETRY_HOME" >> ~/.profile
                echo "export PATH=$POETRY_HOME:$PATH" >> ~/.profile
                . ~/.profile

                poetry --version || exit 1

                poetry self add poetry-plugin-export

                pip install safety
                pip install bandit
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'cd ./banchi/web/static && npm install'
                    sh '''
                    . ~/.profile
                    export PATH="$POETRY_HOME:$PATH"

                    $POETRY_HOME/poetry install
                    $POETRY_HOME/poetry export --without-hashes --format=requirements.txt > requirements.txt
                    '''
                }
            }
        }

        stage('OWASP Dependency-Check Nodejs Package Vulnerabilities') {
            steps {
                sh '''
                . ~/.profile
                export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
                export PATH=$JAVA_HOME/bin:$PATH

                java -version || exit 1
                '''
                dependencyCheck additionalArguments: ''' 
                    --noupdate
                    --out './'
                    --scan './banchi/web/static/package-lock.json'
                    --format 'ALL'
                    --prettyPrint''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities', nvdCredentialsId: 'importstar-nvd-api-key'
                
                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
            }
        }

        stage('Run Safety Dependency-Check Python Package Vulnerabilities') {
            steps {
                script {
                    sh '''
                        safety check -r requirements.txt --full-report --output html > safety_report.html || true
                    '''
                    publishHTML (target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'safety_report.html',
                        reportName: 'Safety Dependency Report'
                    ])
                }
            }
        }


        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${PROJECT_NAME}/${WEB_IMAGE_NAME} ${BO_BUILD_PATH}'
                sh 'docker save ${PROJECT_NAME}/${WEB_IMAGE_NAME} > ${WEB_IMAGE_NAME}.tar'
            }
        }

        stage('Copy image to server') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'binhla2-secret', keyFileVariable: 'SSH_KEY')]) {
                    sh 'scp -P 20222 -i $SSH_KEY ${WEB_IMAGE_NAME}.tar imps@${PRODUCTION_SERVER}:/home/imps/'
                }
            }
        }

        stage('Pull to update in production server and restart service') {
            steps {
                echo 'Pulling..'
                script {
                    remote.user = env.BINHLA_CREDS_USR
                    remote.password = env.BINHLA_CREDS_PSW
                    remote.port=20222
                }
                sshCommand(remote: remote, command: "cd ${PROJECT_PATH} && git pull \
                    && docker load < /home/imps/${WEB_IMAGE_NAME}.tar \
                    && docker compose -f docker-compose-production.yml up -d \
                    && rm /home/imps/${WEB_IMAGE_NAME}.tar"
                )
            }
        }
    }

    post {
        always {
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true,
                    patterns: [[pattern: '.gitignore', type: 'INCLUDE'],
                               [pattern: '.propsfile', type: 'EXCLUDE']])
        }
    }
}
