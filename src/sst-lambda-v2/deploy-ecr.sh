#!/bin/bash
#
# Script to deploy a container image to an AWS Lambda Function
#
# REQUIRES:
#   jq (https://jqlang.github.io/jq/)
#   docker (https://docs.docker.com/desktop/) > version Docker 1.5
#   AWS CLI (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
#
# Command line arguments:
# [1] registry: Registry URI
# [2] repository: Name of repository to create
# [3] prefix: Prefix for environment deploying to
# [4] dockerfile: Name of dockerfile to build container for: "Dockerfile-flpe" or "Dockerfile-moi"
# [5] profile: Name of profile used to authenticate AWS CLI commands
# 
# Example usage: ./deploy-ecr.sh "<account-id>.dkr.ecr.<region>.amazonaws.com" "<container-image-name>" "<confluence-dev1>" "<Dockerfile-flpe>" "<confluence-named-profile>"

REGISTRY=$1
IMAGE_NAME=$2
PREFIX=$3
DOCKERFILE=$4
PROFILE=$5

REPOSITORY=$PREFIX-$IMAGE_NAME

# ECR Repo
response=$(aws ecr describe-repositories --repository-names "$REPOSITORY" --profile "$PROFILE" 2>&1)
if [[ $response == *"RepositoryNotFoundException"* ]]; then
    echo "Respository does not exist. Creating repository: $REPOSITORY."
    # Create repo
    response=$(aws ecr create-repository --repository-name "$REPOSITORY" \
                --image-tag-mutability "MUTABLE" \
                --image-scanning-configuration scanOnPush=false \
                --encryption-configuration encryptionType="AES256" \
                --profile "$PROFILE" )
    
    # Test if repo was created
    status=$(echo "$response" | jq '.repository.repositoryName')
    status="${status%\"}"    # Remove suffix double quote
    status="${status#\"}"    # Remove prefix double quote
    if [[ "$status" == "$REPOSITORY" ]]; then
        echo "Repository was created."
    else
        echo "Respository could not be created."
        echo "Response: $response"
        exit 1
    fi
else
    repo=$(echo "$response" | jq '.repositories[0].repositoryName')
    repo="${repo%\"}"    # Remove suffix double quote
    repo="${repo#\"}"    # Remove prefix double quote
    echo "Repository exists: '$REPOSITORY' and will not be created."
fi

# Login
docker login -u AWS https://$REGISTRY -p $(aws --profile $PROFILE ecr get-login-password --region us-west-2)

# Build
#cd ..
docker build -t $REGISTRY/$REPOSITORY -f $DOCKERFILE .

# # Push
docker push $REGISTRY/$REPOSITORY
#cd deploy
