variable "app_name" {
  type        = string
  description = "Application name"
  default     = "SST"
}

variable "aws_region" {
  type        = string
  description = "AWS region to deploy to"
  default     = "us-west-2"
}

variable "default_tags" {
  type    = map(string)
  default = {}
}

variable "ecr_repo_one" {
  type        = string
  description = "sst-lambda-explode container image repository name"
}

variable "ecr_repo_two" {
  type        = string
  description = "sst-lambda-write container image repository name"
}

variable "ecr_repo_three" {
  type        = string
  description = "sst-lambda-stats container image repository name"
}

variable "ecr_repo_four" {
  type        = string
  description = "sst-lambda-grid container image repository name"
}

variable "edl_password" {
  type        = string
  description = "Earthdata Login password"
}

variable "edl_username" {
  type        = string
  description = "Earthdata Login useranme"
}

variable "lambda_role" {
  type        = string
  description = "Name of AWS Lambda IAM role"
}

variable "prefix" {
  type        = string
  description = "Prefix to add to all AWS resources as a unique identifier"
}

variable "profile" {
  type        = string
  description = "Named profile to build infrastructure with"
}