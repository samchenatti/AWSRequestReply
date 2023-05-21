resource "aws_api_gateway_rest_api" "integration_gateway" {
  body = jsonencode({
    openapi = "3.0.1"
    info = {
      title   = "integration_gateway"
      version = "1.0"
    }
    paths = {
      "/tenants/{tenant_uuid}/predict" = {
        post = {
          responses = {
            "200" = {
              description = "Event posted"
            }
          }

          x-amazon-apigateway-integration = {
            httpMethod           = "POST"
            payloadFormatVersion = "1.0"
            type                 = "AWS"
            uri                  = "arn:aws:apigateway:sa-east-1:sqs:path/{tenant_uuid}-integration-queue"
            credentials          = aws_iam_role.gateway_role.arn

            responses = {
              default = {
                statusCode = 200
              }
            }

            passthroughBehavior = "never"

            requestParameters = {
              "integration.request.header.Content-Type" = "'application/x-www-form-urlencoded'"
              "integration.request.path.tenant_uuid" = "method.request.path.tenant_uuid"
            }

            requestTemplates = {
              "application/json" = "Action=SendMessage&MessageBody=$input.body"
            }
          }
        }
      }
    }
  })

  name = "integration_gateway"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_deployment" "integration_gateway" {
  rest_api_id = aws_api_gateway_rest_api.integration_gateway.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.integration_gateway.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "integration_gateway" {
  deployment_id = aws_api_gateway_deployment.integration_gateway.id
  rest_api_id   = aws_api_gateway_rest_api.integration_gateway.id
  stage_name    = "dev"
}