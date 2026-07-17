pipeline {
    agent any

    options {
        timestamps()
        ansiColor('xterm')
    }

    environment {
        AWS_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID = '655383751644'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        AUTH_REPO = "streamingapp-auth"
        ADMIN_REPO = "streamingapp-admin"
        CHAT_REPO = "streamingapp-chat"
        STREAMING_REPO = "streamingapp-streaming"
        FRONTEND_REPO = "streamingapp-frontend"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

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

                echo
                echo "========== Repository =========="
                ls -la

                echo
                echo "========== Backend =========="
                ls -la backend

                echo
                echo "========== Package.json =========="
                find . -name package.json

                echo
                echo "========== Dockerfiles =========="
                find . -name Dockerfile
                '''
            }
        }

        stage('Cleanup Docker Cache') {
            steps {
                sh '''
                echo "Cleaning Docker cache..."

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

        stage('List Local Images') {
            steps {
                sh '''
                docker images | grep streamingapp || true
                '''
            }
        }

        stage('Login to Amazon ECR') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-ecr-creds']
                ]) {
                    sh '''
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login \
                        --username AWS \
                        --password-stdin \
                        ${ECR_REGISTRY}
                    '''
                }
            }
        }

        stage('Tag Images') {
            steps {
                sh '''
                docker tag streamingapp-auth:latest ${ECR_REGISTRY}/${AUTH_REPO}:latest
                docker tag streamingapp-admin:latest ${ECR_REGISTRY}/${ADMIN_REPO}:latest
                docker tag streamingapp-chat:latest ${ECR_REGISTRY}/${CHAT_REPO}:latest
                docker tag streamingapp-streaming:latest ${ECR_REGISTRY}/${STREAMING_REPO}:latest
                docker tag streamingapp-frontend:latest ${ECR_REGISTRY}/${FRONTEND_REPO}:latest
                '''
            }
        }

        stage('Push Auth Image') {
            steps {
                sh '''
                docker push ${ECR_REGISTRY}/${AUTH_REPO}:latest
                '''
            }
        }

        stage('Push Admin Image') {
            steps {
                sh '''
                docker push ${ECR_REGISTRY}/${ADMIN_REPO}:latest
                '''
            }
        }

        stage('Push Chat Image') {
            steps {
                sh '''
                docker push ${ECR_REGISTRY}/${CHAT_REPO}:latest
                '''
            }
        }

        stage('Push Streaming Image') {
            steps {
                sh '''
                docker push ${ECR_REGISTRY}/${STREAMING_REPO}:latest
                '''
            }
        }

        stage('Push Frontend Image') {
            steps {
                sh '''
                docker push ${ECR_REGISTRY}/${FRONTEND_REPO}:latest
                '''
            }
        }

        stage('Verify Images in ECR') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-ecr-creds']
                ]) {
                    sh '''
                    aws ecr describe-images \
                        --repository-name ${AUTH_REPO} \
                        --region ${AWS_REGION}

                    aws ecr describe-images \
                        --repository-name ${ADMIN_REPO} \
                        --region ${AWS_REGION}

                    aws ecr describe-images \
                        --repository-name ${CHAT_REPO} \
                        --region ${AWS_REGION}

                    aws ecr describe-images \
                        --repository-name ${STREAMING_REPO} \
                        --region ${AWS_REGION}

                    aws ecr describe-images \
                        --repository-name ${FRONTEND_REPO} \
                        --region ${AWS_REGION}
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '======================================'
            echo 'CI Pipeline completed successfully!'
            echo 'All Docker images have been pushed to Amazon ECR.'
            echo '======================================'
        }

        failure {
            echo '======================================'
            echo 'Pipeline failed.'
            echo '======================================'
        }
    }
}