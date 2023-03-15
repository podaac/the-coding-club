# sst

The sst program compare various SST data products and produces stats.

## aws infrastructure

The sst program includes the following AWS services:
- Lambda function to execute code deployed via zip file.

## terraform 

Deploys AWS infrastructure and stores state in an S3 backend.

To deploy:
1. Edit `terraform.tfvars` for environment to deploy to.
3. Initialize terraform: `terraform init`
4. Plan terraform modifications: `terraform plan -out=tfplan`
5. Apply terraform modifications: `terraform apply tfplan`