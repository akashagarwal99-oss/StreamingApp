pipeline {
    agent any

    options {
        timestamps()
    }

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
                    sh '''
                    aws sts get-caller-identity
                    '''
                }
            }
        }

        stage('Inspect Workspace') {
            steps {
                sh '''
                echo "========== Current Directory =========="
                pwd

                echo ""
                echo "========== Root =========="
                ls -la

                echo ""
                echo "========== Backend =========="
                ls -la backend

                echo ""
                echo "========== Package.json Files =========="
                find . -name package.json

                echo ""
                echo "========== Dockerfiles =========="
                find . -name Dockerfile
                '''
            }
        }

        stage('Cleanup Docker Cache') {
            steps {
                sh '''
                echo "Cleaning unused Docker cache..."

                docker builder prune -f || true
                docker image prune -f || true

                docker system df
                '''
            }
        }

        stage('Build Auth Image') {
            steps {
                sh '''
                docker build \
                  -t streamingapp-auth:latest \
                  backend/authService
                '''
            }
        }

        stage('Build Admin Image') {
            steps {
                sh '''
                docker build \
                  -t streamingapp-admin:latest \
                  -f backend/adminService/Dockerfile \
                  backend
                '''
            }
        }

        stage('Build Chat Image') {
            steps {
                sh '''
                docker build \
                  -t streamingapp-chat:latest \
                  -f backend/chatService/Dockerfile \
                  backend
                '''
            }
        }

        stage('Build Streaming Image') {
            steps {
                sh '''
                docker build \
                  -t streamingapp-streaming:latest \
                  -f backend/streamingService/Dockerfile \
                  backend
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                export NODE_OPTIONS=--max-old-space-size=1024

                docker build \
                  -t streamingapp-frontend:latest \
                  frontend
                '''
            }
        }

        stage('List Images') {
            steps {
                sh '''
                echo ""
                echo "========== Docker Images =========="

                docker images | grep streamingapp || true
                '''
            }
        }
    }

    post {
        success {
            echo 'All Docker images built successfully!'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}