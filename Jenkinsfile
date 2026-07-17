pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
    }

    stages {

        stage('Verify AWS Credentials') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                     credentialsId: 'aws-ecr-creds']
                ]) {
                    sh 'aws sts get-caller-identity'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {

                    def backendServices = [
                        [name: 'auth', dockerfile: 'backend/authService/Dockerfile'],
                        [name: 'admin', dockerfile: 'backend/adminService/Dockerfile'],
                        [name: 'chat', dockerfile: 'backend/chatService/Dockerfile'],
                        [name: 'streaming', dockerfile: 'backend/streamingService/Dockerfile']
                    ]

                    backendServices.each { service ->
                        sh """
                            docker build \
                              -t streamingapp-${service.name}:latest \
                              -f ${service.dockerfile} \
                              backend
                        """
                    }

                    sh """
                        docker build \
                          -t streamingapp-frontend:latest \
                          frontend
                    """
                }
            }
        }

        stage('List Images') {
            steps {
                sh 'docker images | grep streamingapp'
            }
        }
    }

    post {
        success {
            echo 'Docker images built successfully!'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}