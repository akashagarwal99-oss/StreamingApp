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

        stage('Inspect Workspace') {
            steps {
                sh '''
                    echo "================ CURRENT DIRECTORY ================"
                    pwd

                    echo ""
                    echo "================ ROOT FILES ================"
                    ls -la

                    echo ""
                    echo "================ BACKEND ================"
                    ls -la backend

                    echo ""
                    echo "================ AUTH SERVICE ================"
                    ls -la backend/authService

                    echo ""
                    echo "================ ADMIN SERVICE ================"
                    ls -la backend/adminService

                    echo ""
                    echo "================ CHAT SERVICE ================"
                    ls -la backend/chatService

                    echo ""
                    echo "================ STREAMING SERVICE ================"
                    ls -la backend/streamingService

                    echo ""
                    echo "================ PACKAGE.JSON FILES ================"
                    find . -name package.json

                    echo ""
                    echo "================ DOCKERFILES ================"
                    find . -name Dockerfile
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                script {

                    // Auth Service
                    sh '''
                        docker build \
                            -t streamingapp-auth:latest \
                            backend/authService
                    '''

                    // Admin Service
                    sh '''
                        docker build \
                            -t streamingapp-admin:latest \
                            -f backend/adminService/Dockerfile \
                            backend
                    '''

                    // Chat Service
                    sh '''
                        docker build \
                            -t streamingapp-chat:latest \
                            -f backend/chatService/Dockerfile \
                            backend
                    '''

                    // Streaming Service
                    sh '''
                        docker build \
                            -t streamingapp-streaming:latest \
                            -f backend/streamingService/Dockerfile \
                            backend
                    '''

                    // Frontend
                    sh '''
                        docker build \
                            -t streamingapp-frontend:latest \
                            frontend
                    '''
                }
            }
        }

        stage('List Images') {
            steps {
                sh 'docker images | grep streamingapp || true'
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

        always {
            cleanWs()
        }
    }
}