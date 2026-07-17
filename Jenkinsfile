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
                    sh '''
                        aws sts get-caller-identity
                    '''
                }
            }
        }
    }
}