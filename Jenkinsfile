pipeline {
    agent any
    environment{
        aws_region="ap-south-1",
        aws_cred='awsLogin',
        s3_bkt='devops-jenkins-github-s1',
        s3_key='lambda_handler.zip',
        lambda_func="lambdaoverhttps"
    }

    stages {
        stage('Check out Github') {
            steps {
                checkout scm
            }
        }
        stage('Zip the lambda code') {
            steps {
                sh '''
                    rm -f lambda_handler.zip
                    zip lambda_handler.zip lambda_handler.py
                '''
            }
        }
        stage('Pushing to S3 bucket') {
            steps {
                sh '''
                    withAWS(credentials:'${aws_cred}', region:'${aws_region}'){
                        aws s3 cp lambda_handler.zip s3://$s3_bkt/$s3_key
                    }
                '''
            }
        }
        stage('Deploying lambda function') {
            steps {
                sh '''
                        withAWS(credentials:'${aws_cred}'){
                        aws lambda get-function --function-name $lambda_func 
                        if [ 0 -eq $? ]; then
                            echo "Lambda '$1' exists"
                            aws lambda update-function-code \
                                --function-name $lambda_func \
                                --s3-bucket $s3_bkt \
                                --s3-key $s3_key
                        else
                            echo "Lambda '$1' does not exist"
                            aws create-function \
                                --function-name $lambda_func \
                                --runtime python3.9 \
                                --role arn:aws:iam::065526474072:role/lambda-apigateway-role \
                                --handler lambda_handler.lambda_handler \
                                --code S3Bucket=$s3_bkt,S3Key=$s3_key \
                                --timeout 20 \
                                --memory-size 128
                        fi
                    }
                }
                '''
            }
        }
        post{
                always {
                    echo 'Pipeline finished.'
                }
                success {
                    echo 'Deployment successful!'
                }

                failure {
                    echo 'Something went wrong.'
                }

            }
 
    }
}
