pipeline {
    agent any
    
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
        stage('Test Parameter') {
            steps {
                echo "${params.IMAGE_TAG}"
            }
        }
    }
}