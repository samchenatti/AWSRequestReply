resource "aws_iam_role" "gateway_role" {
  name = "gateway_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      }
    ]
  })

  inline_policy {
    name = "sqs_policy"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = "sqs:*"
          Effect   = "Allow"
          Sid      = ""
          Resource = "arn:aws:sqs:sa-east-1:*:*-requests-queue"
        }
      ]
    })
  }
}
