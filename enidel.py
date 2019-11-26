import boto3, json
from time import sleep
from botocore.exceptions import ClientError

def listeni(region, context):
    enilist = []
    ec2 = boto3.client("ec2", region_name=region)
    lambdafilters = [{'Name': 'status', 'Values': ['available']}, {'Name': 'description', 'Values': ['AWS Lambda VPC ENI*']}]
    paginator = ec2.get_paginator('describe_network_interfaces')
    page_iterator = paginator.paginate(Filters=lambdafilters)
    for page in page_iterator:
        enilist = enilist + [eni['NetworkInterfaceId'] for eni in page['NetworkInterfaces']]
    if enilist:
        deleni(region, ec2, enilist, context)

def deleni(region, client, enilist, context):
    fn_region = context.invoked_function_arn.split(":")[3]
    for eni in enilist:
        if context.get_remaining_time_in_millis() <= 2000:
            lam = boto3.client("lambda", region_name=fn_region)
            lam.invoke(
                FunctionName=context.function_name,
                InvocationType='Event',
                Payload = bytes(json.dumps({'region': region}), encoding='utf8'))
            print(f"Another Function Invoked. Remaining time - {context.get_remaining_time_in_millis()/1000} seconds")
            break
        else:
            try:
                client.delete_network_interface(NetworkInterfaceId=eni)
                print (f"Lambda ENI: {eni} is deleted")
            except ClientError as e:
                if e.response['Error']['Code'] in ('ThrottlingException', 'RequestLimitExceeded'):
                    sleep(3)
                    continue
                if e.response['Error']['Code'] == 'InvalidNetworkInterfaceID.NotFound':
                    continue

def lambda_handler(event, context):
    region = event['region']
    listeni(region, context)