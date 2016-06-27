# lambda_slack_aws_billing

This is a AWS Lambda function which posts AWS billing info to slack.

![billing bot](https://github.com/azaazato/lambda_slack_aws_billing/blob/master/bot_image.png)


## Usage

Set your environment HOOK_URL and SALCK_CHANNEL.

```
# set your own environment
HOOK_URL = 'https://hooks.slack.com/services/xxxxxxxxxxxxxxxx'
SLACK_CHANNEL = '#xxxxxxxxxx'
```

After set above items, deploy to your aws environmet. Set scheduled Event to post slack everyday.

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[azaazato](https://github.com/azaazato)
