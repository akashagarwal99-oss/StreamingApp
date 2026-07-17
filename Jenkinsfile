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

                    def services = [
                        [name: 'auth', context: 'backend/authService'],
                        [name: 'admin', context: 'backend/adminService'],
                        [name: 'chat', context: 'backend/chatService'],
                        [name: 'streaming', context: 'backend/streamingService'],
                        [name: 'frontend', context: 'frontend']
                    ]

                    services.each { service ->
                        sh """
                            docker build \
                              -t streamingapp-${service.name}:latest \
                              ${service.context}
                        """
                    }

                }
            }
        }

        stage('List Images') {
            steps {
                sh 'docker images | grep streamingapp'
            }
        }
    }
}