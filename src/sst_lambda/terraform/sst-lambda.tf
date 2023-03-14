# AWS Lambda function
resource "aws_lambda_function" "aws_lambda_error_handler" {
  image_uri     = "${data.aws_ecr_repository.podaac_sst_repo.repository_url}:latest"
  function_name = "${var.prefix}-sst"
  role          = data.aws_iam_role.lambda_execution_role.arn
  package_type  = "Image"
  memory_size   = 256
  timeout       = 900
}