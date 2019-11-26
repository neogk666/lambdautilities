import boto3
from datetime import datetime, timedelta

def list_functions(region, metric, hours, context):
    funclist = []
    datadict = {"Functions": []}
    if metric not in ("Invocations", "Throttles", "Errors", "Duration"):
        print ("Metric should be either 'Invocations', 'Throttles', 'Errors' or 'Duration'")
        return
    cloudwatch = boto3.client('cloudwatch', region)
    paginator = cloudwatch.get_paginator('list_metrics')
    response_iterator = paginator.paginate(
        Namespace='AWS/Lambda',
        MetricName=metric)
    for page in response_iterator:
        if context.get_remaining_time_in_millis() <= 2000:
            break
        else:
            funclist = funclist + list(set([func['Dimensions'][0]['Value'] for func in page['Metrics'] if func['Dimensions']]))
            for func in funclist:
                childdict = get_throttle(cloudwatch, region, func, metric, hours)
                datadict['Functions'].append(childdict)
    return datadict

def get_throttle(client, region, function, metric, hour):
    now = datetime.fromtimestamp(float(datetime.utcnow().strftime("%s")))
    start = datetime.fromtimestamp(float((datetime.utcnow() - timedelta(hours=hour)).strftime("%s")))
    if metric == 'Duration':
        unit = 'Milliseconds'
        stat = 'Average'
    else:
        unit = 'Count'
        stat = 'Sum'
    data = client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName=metric,
        Dimensions=[
           { 'Name': 'FunctionName',
             'Value': function
           }
        ],
        StartTime=start.strftime('%Y-%m-%dT%H:%M:%SZ'),
        EndTime=now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        Period=hour*60*60,
        Statistics=[stat],
        Unit=unit
    )
    if data['Datapoints']:
        childdict = {'FunctionName':function, "Metric":metric, "Total":int(data['Datapoints'][0][stat])}
    else:
        childdict = {'FunctionName':function, "Metric":metric, "Total":0}
    return childdict

def tohtml(region, datadict, hours, metric):
    sorted_dict = sorted(datadict, key=lambda k: k['Total'], reverse=True)
    if metric == 'Duration':
        metric = 'Duration (in Milliseconds)'
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
        <h1>Region: """ + region + """</h1>
        <h2>Last """ + str(hours) + """ hours</h2>
        <body leftmargin="100">
            <table border=1>
                <tr>
                    <th>Function</th>
                    <th>""" + metric + """</th>
                </tr>
            <indent>"""
    for func in sorted_dict:
        message += """
                <tr>
                    <td>""" + func['FunctionName'] + """</td>
                    <td>""" + str(func['Total']) + """</td>
                </tr>"""
    message += """</indent>
            </table>
        </body></html>"""
    return message

def lambda_handler(event, context):
    region = event['queryStringParameters']['region']
    metric = event['queryStringParameters']['type']
    hours = int(event['queryStringParameters']['hours'])
    datadict = list_functions(region, metric, hours, context)
    message = tohtml(region, datadict['Functions'], hours, metric)
    return {
    'isBase64Encoded': False,
    'statusCode': 200,
    'headers': { "Content-Type": "text/html"},
    'body': message }