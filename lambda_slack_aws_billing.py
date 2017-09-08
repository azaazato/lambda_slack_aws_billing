# coding:utf-8
from __future__ import print_function
import boto3
import datetime
import json
import os
import logging
from urllib2 import Request, urlopen, URLError, HTTPError

# set your own environment
HOOK_URL = os.getenv("HOOK_URL")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
CLOUD_WATCH_REGION = os.getenv("CLOUD_WATCH_REGION") 

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('cloudwatch', region_name=CLOUD_WATCH_REGION, endpoint_url='http://monitoring.'+ CLOUD_WATCH_REGION  +'.amazonaws.com')


def get_billing():
    start_date = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(1), datetime.time())
    params = {
            'MetricName': 'EstimatedCharges',
            'Namespace': 'AWS/Billing',
            'Period': 86400,
            'StartTime': start_date,
            'EndTime': datetime.datetime.combine(datetime.date.today(), datetime.time()),
            'Statistics': ['Maximum'],
            'Dimensions': [
                {
                    'Name': 'Currency',
                    'Value': 'USD'
                }
            ]
    }
    res = client.get_metric_statistics(**params)
    print(res)
    if (res['ResponseMetadata']['HTTPStatusCode'] != 200):
        logger.error('Failed to get billing metrics.')
        exit(1)
    billing = res['Datapoints'][0]['Maximum']
    return billing


def post_slack(date, billing):
    message = {
            'text': "Total estimated charges for AWS04  on {} is US${}".format(date, billing)
            }
    req = Request(HOOK_URL, json.dumps(message))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to")
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
        exit(1)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
        exit(1)


def lambda_handler(event, context):
    billing = get_billing()
    yesterday = datetime.date.today() - datetime.timedelta(1)
    post_slack(yesterday.strftime("%Y-%m-%d"), billing)