import boto3
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

def find_logs(region, function, hour):
    datadict = {"LogStreams": []}
    logs = boto3.client('logs', region)
    startepoch = int((datetime.utcnow() - timedelta(hours=hour)).strftime("%s"))
    logGroupName = '/aws/lambda/us-east-1.' + function
    paginator = logs.get_paginator('describe_log_streams')
    response_iterator = paginator.paginate(
        logGroupName=logGroupName,
        orderBy='LastEventTime',
        descending=True
        )
    try:
        for page in response_iterator:
            for stream in page['logStreams']:
                if 'lastEventTimestamp' in stream:
                    logdate = int(str(stream['lastEventTimestamp'])[:-3])
                    if (logdate > startepoch):
                        link = 'https://' + region + '.console.aws.amazon.com/cloudwatch/home?region=' + region + '#logEventViewer:group=/aws/lambda/us-east-1.' + function + ';stream=' + stream['logStreamName']
                        childdict = {'StreamName':stream['logStreamName'], "Date":logdate, "Link":link, 'Region':region}
                        datadict['LogStreams'].append(childdict)
    except logs.exceptions.ResourceNotFoundException: pass
    return datadict['LogStreams']

def tohtml(function, datadict, hours):
    sorted_dict = sorted(datadict, key=lambda k: k['Date'], reverse=True)
    message = """<html>
        <head><style>
            body {background-color: lightgoldenrodyellow;}
            h1 {color:#ed3330;
                font-family: verdana,arial,sans-serif;
                font-size:25px;}
            h2 {color:#ed3330;
                font-family: verdana,arial,sans-serif;
                font-size:20px;}
            table {
                font-family: verdana,arial,sans-serif;
                font-size:12px;
                color:#333333;
                border-width: 1px;
                border-color: #666666;
                border-collapse: collapse;}
            table th {
                border-width: 1px;
                padding: 8px;
                border-style: solid;
                border-color: #666666;
                background-color: #dedede;}
            table td {
                border-width: 1px;
                padding: 8px;
                border-style: solid;
                border-color: #666666;
                background-color: #ffffff;}
        </style></head>
        <h1>Function Name: """ + function + """</h1>
        <h2>Last """ + str(hours) + """ hours</h2>
        <body leftmargin="100">
            <table border=1>
                <tr>
                    <th>Date</th>
                    <th>Log Stream Name</th>
                    <th>Region</th>
                </tr>
            <indent>"""
    for stream in sorted_dict:
        message += """
                <tr>
                    <td>""" + time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(stream['Date'])) + """</td>
                    <td><a href=\"""" + stream['Link'] + """\">""" + stream['StreamName'] + """</a></td>
                    <td>""" + stream['Region'] + """</td>
                </tr>"""
    message += """</indent>
            </table>
        </body></html>"""
    return message

def lambda_handler(event, context):
    function = event['queryStringParameters']['function']
    hours = int(event['queryStringParameters']['hours'])
    ec2 = boto3.client('ec2')
    datalist = []
    regions = ec2.describe_regions()['Regions']
    with ThreadPoolExecutor(max_workers=len(regions)) as exec:
        futures = [exec.submit(find_logs, region['RegionName'], function, hours) for region in regions]
        exec.shutdown(False)
        for fut in as_completed(futures):
            try:
                #datalist.append(fut.result())
                datalist += fut.result()
            except Exception as e:
                print (e)
    message = tohtml(function, datalist, hours)
    return {
    'isBase64Encoded': False,
    'statusCode': 200,
    'headers': { "Content-Type": "text/html"},
    'body': message }