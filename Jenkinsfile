pipeline {
    agent any
    environment {
        DOCKERHUB_USERNAME = "idrisniyi94"
        DEPLOYMENT_NAME = "devops-enterprise-web"
        IMAGE_NAME = "${env.DOCKERHUB_USERNAME}/devops-enterprise-web:${params.IMAGE_TAG}"
        // IMAGE_TAG = "${params.BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = credentials('d4506f04-b98c-47db-95ce-018ceac27ba6')
        SCANNER_HOME = tool 'sonar-scanner'
    }
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Git Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/stwins60/DevopsEnterprise.git'
            }
        }
        stage('Sonarqube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') {
                        sh "$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectKey=devops-enterprise -Dsonar.sources=. -Dsonar.host.url=http://192.168.0.43:9000 -Dsonar.login=sqp_091aaedd555a59acfc5c9726c6033575a52d310f"
                    }
                }
            }
        }
        stage('Pytest') {
            steps {
                sh "pip install -r requirements.txt --no-cache-dir"
                sh "ls -l"
                sh "python3 -m pytest test_app.py"
            }
        }
        stage('Trivy File Scan') {
            steps {
                sh "docker run --rm aquasec/trivy:0.18.3 fs ."
            }
        }
        stage('DockerHub Login') {
            steps {
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                echo "Login Succeeded"
            }
        }
        stage("Docker Build") {
            steps {
                script {
                    def imageName = "${env.IMAGE_NAME}"
                    def command = "docker image inspect $imageName"
                    def returnStatus = sh(script:command, returnStatus: true)

                    if (returnStatus == 0) {
                        echo "Image Exist. Skipping"
                    } else {
                        echo "Building the Docker Image"
                        def buildCommand = "docker build -t $imageName ."
                        sh(script: buildCommand)
                    }
                }
            }
        }
        stage("Trivy Image Scan") {
            steps {
                sh "docker run -u 0 --rm aquasec/trivy:0.18.3 ${env.IMAGE_NAME}"
            }
        }
        stage("Push Image to DockerHub") {
            steps {
                sh "docker push ${env.IMAGE_NAME}"
            }
        }
    }
}