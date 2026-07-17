pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Repository cloned successfully!'
            }
        }

        stage('Verify Tools') {
            steps {
                sh 'docker --version'
                sh 'aws --version'
                sh 'kubectl version --client'
                sh 'helm version'
            }
        }

        stage('Success') {
            steps {
                echo 'Jenkins Pipeline is working!'
            }
        }
    }
}