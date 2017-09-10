# lambda_slack_aws_billing

This is a AWS Lambda function written in python 2.7 which posts detailed AWS billing info to slack.


## Usage

Set your environment CLOUD_WATCH_REGION, AWS_SERVICE(name), HOOK_URL and SALCK_CHANNEL values.

Please note cloudwatch billing monitoring API is only available in N.Virginia / us-east-1

After setting  theabove items, deploy it to your aws environmet. Set scheduled Event to post slack everyday.


## Add the lambda role from root in N.Virginia to get access for billing.

Provide role with the appropriate AWS billing and cloudwatch access.

The IAM policy used is as follows:

`{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cloudwatch:*"
            ],
            "Resource": "*",
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "true"
                }
            }
        }
    ]
}`

Also please follow the instructions here - https://www.youtube.com/watch?v=ERKPy-wEnF8

## Modified from

[azaazato](https://github.com/azaazato)



