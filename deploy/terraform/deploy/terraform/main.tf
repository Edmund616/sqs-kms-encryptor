provider "aws" {
  region = "us-east-1" # Change to your preferred region
}

# ------------------------
# KMS Key for SQS Encryption
# ------------------------
resource "aws_kms_key" "sqs_key" {
  description             = "KMS key for SQS encryption"
  deletion_window_in_days = 7
  enable_key_rotation     = true
}

# ------------------------
# IAM Role for Lambda
# ------------------------
resource "aws_iam_role" "lambda_exec" {
  name = "sqs-kms-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# ------------------------
# IAM Policy for Lambda
# ------------------------
resource "aws_iam_policy" "lambda_policy" {
  name = "sqs-kms-access-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "sqs:ListQueues",
          "sqs:GetQueueAttributes",
          "sqs:SetQueueAttributes"
        ],
        Effect = "Allow",
        Resource = "*"
      },
      {
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:GenerateDataKey*"
        ],
        Effect = "Allow",
        Resource = "*"
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect = "Allow",
        Resource = "*"
      }
    ]
  })
}

# ------------------------
# Attach Policy to Role
# ------------------------
resource "aws_iam_role_policy_attachment" "attach_lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# ------------------------
# Lambda Function
# ------------------------
resource "aws_lambda_function" "sqs_kms_encryptor" {
  function_name = "sqs-kms-encryptor"
  handler       = "app.lambda_handler"
  runtime       = "python3.12"

  filename         = "${path.module}/../../lambda/sqs_encryptor.zip"
  source_code_hash = filebase64sha256("${path.module}/../../lambda/sqs_encryptor.zip")

  role = aws_iam_role.lambda_exec.arn

  environment {
    variables = {
      KMS_KEY_ARN = aws_kms_key.sqs_key.arn
    }
  }
}
