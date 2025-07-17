# sqs-kms-encryptor

This project encrypts all SQS queues in an AWS account using a specified KMS key.  
It can run as a Lambda function or via CLI.

## Structure

- `src/`: Main logic
- `lambda/`: Lambda handler
- `deploy/`: Terraform and SAM deployment options

## Usage

### Lambda
- Deploy using `deploy/terraform` or `deploy/sam`

### CLI
```bash
python src/main.py


---

### 📁 `deploy/terraform/main.tf`

```bash
mkdir -p deploy/terraform
nano deploy/terraform/main.tf

provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_function" "encryptor" {
  filename         = "function.zip"
  function_name    = "sqs-kms-encryptor"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.11"
  source_code_hash = filebase64sha256("function.zip")
}
