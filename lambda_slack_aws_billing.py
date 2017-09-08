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
AWS_SERVICE = os.getenv("AWS_SERVICE") 

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('cloudwatch', region_name=CLOUD_WATCH_REGION, endpoint_url='http://monitoring.'+ CLOUD_WATCH_REGION  +'.amazonaws.com')


def get_billing_total(start_date, end_date):
    params = {
            'MetricName': 'EstimatedCharges',
            'Namespace': 'AWS/Billing',
            'Period': 86400,
            'StartTime': start_date,
            'EndTime': end_date,
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
    if len(res['Datapoints']) > 0:
        billing = res['Datapoints'][0]['Maximum']
    else:
        billing = 0.0
    return  str(billing)
	
def get_billing_field(start_date, end_date, field):
    params = {
            'MetricName': 'EstimatedCharges',
            'Namespace': 'AWS/Billing',
            'Period': 86400,
            'StartTime': start_date,
            'EndTime': end_date,
            'Statistics': ['Maximum'],
            'Dimensions': [
                {
                    'Name': 'Currency',
                    'Value': 'USD'
                },
                {
                    'Name': 'ServiceName',
                    'Value': field
                }
            ]
    }
    res = client.get_metric_statistics(**params)
    print(res)
    if (res['ResponseMetadata']['HTTPStatusCode'] != 200):
        logger.error('Failed to get billing metrics.')
        exit(1)
    if len(res['Datapoints']) > 0:
        billing = res['Datapoints'][0]['Maximum']
    else:
        billing = 0.0
    return str(billing)

	
def post_slack(message):
    message = {
            'text': message,
			'channel': SLACK_CHANNEL
            }
    req = Request(HOOK_URL, json.dumps(message))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to slack.")
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
        exit(1)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
        exit(1)

		
def generate_slack_message(start_date, end_date):
	AWSDataTrensfer = get_billing_field(start_date, end_date, 'AWSDataTrensfer')
	AWSLambda = get_billing_field(start_date, end_date, 'AWSLambda')
	AWSMarketplace = get_billing_field(start_date, end_date, 'AWSMarketplace')
	AWSQueueService = get_billing_field(start_date, end_date, 'AWSQueueService')
	AWSCloudWatcha = get_billing_field(start_date, end_date, 'AmazonCloudWatcha')
	AWSEC2 = get_billing_field(start_date, end_date, 'AmazonEC2')
	AWSS3 = get_billing_field(start_date, end_date, 'AmazonS3')
	AWSSNS = get_billing_field(start_date, end_date, 'AmazonSNS')
	awskms = get_billing_field(start_date, end_date, 'awskms')
	total = get_billing_total(start_date, end_date)
	formatted_start_date = start_date.strftime("%Y-%m-%d")
	formatted_end_date = end_date.strftime("%Y-%m-%d")
	
	message = 'Estimated charges for ' + AWS_SERVICE + ' between ' + formatted_start_date + ' to ' + formatted_end_date + ' is as follows: \n\n' + 'AWS Data Trensfer                       US$ ' + AWSDataTrensfer + ' \n' + 'AWS Lambda                                 US$ ' + AWSLambda + ' \n' + 'AWS Marketplace                         US$ ' + AWSMarketplace + ' \n' + 'AWS Queue Service                     US$ ' + AWSQueueService + ' \n' + 'AWS Cloud Watch                        US$ ' + AWSCloudWatcha + ' \n' + 'AWS EC2                                       US$ ' + AWSEC2 + ' \n' + 'AWS S3                                          US$ ' + AWSS3 + ' \n' + 'AWS SNS                                       US$ ' + AWSSNS + ' \n' + 'AWS Key Management Service   US$ ' + awskms + ' \n' + '-------------------------------------------\n' + 'Total                                               US$ ' + total
	return message
	

def lambda_handler(event, context):
	start_date = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(1), datetime.time())
	end_date = datetime.datetime.combine(datetime.date.today(), datetime.time())
	message = generate_slack_message(start_date, end_date)
	post_slack(message)