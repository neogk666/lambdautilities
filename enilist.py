import boto3, json
from time import sleep
from botocore.exceptions import ClientError

def listeni(region, op, status, context):
    enilist = []
    def get_value(status):
        return {
            'Available': ['available'],
            'In-use': ['in-use'],
            'All': ['available', 'in-use']
        }.get(status)
    ec2 = boto3.client("ec2", region_name=region)
    lambdafilters = [{'Name': 'status', 'Values': get_value(status)}, {'Name': 'description', 'Values': ['AWS Lambda VPC ENI*']}]
    paginator = ec2.get_paginator('describe_network_interfaces')
    page_iterator = paginator.paginate(Filters=lambdafilters)
    for page in page_iterator:
        enilist = enilist + [eni for eni in page['NetworkInterfaces']]
    message = ''
    if op == 'List':
        message = tohtml(region, enilist)
    elif op == 'Delete':
        if status in ('All', 'In-use'):
            msg = "Operation NOT supported. Deletion is only supported with 'Availale' ENIs"
            message = tohtml2(region, msg) 
        elif status == 'Available':
            msg = enidelete(region, context)
            #msg = "Deletion task has been submitted. This is an asynchronous operation, and will take few seconds to minutes. List the ENI again to see the status."
            message = tohtml2(region, msg)
    else:
        msg = "Choose either 'List' or 'Delete' Operation"
        message = tohtml2(region, msg)
    return message

def enidelete(region, context):
    fn_region = context.invoked_function_arn.split(":")[3]
    lam = boto3.client("lambda", region_name=fn_region)
    response_iterator = lam.get_paginator('list_functions').paginate()
    fn_list = [fn['FunctionArn'] for page in response_iterator for fn in page['Functions'] if 'LambdaENIDelFn' in fn['FunctionName']]
    #fn_list = [fn['FunctionArn']  if 'LambdaENIDelFn' in fn['FunctionName'] else '' for page in response_iterator for fn in page['Functions']]
    src_stack_id = lam.list_tags(Resource=context.invoked_function_arn)['Tags']['aws:cloudformation:stack-id'].split(":")[-1].split("/")[-1]
    fn_name = ''
    for fn in fn_list:
        dest_stack_id = lam.list_tags(Resource=fn)['Tags']['aws:cloudformation:stack-id'].split(":")[-1].split("/")[-1]
        if src_stack_id == dest_stack_id:
            fn_name = fn.split(":")[6]
            break
    lam.invoke(
        FunctionName=fn_name,
        InvocationType='Event',
        Payload = bytes(json.dumps({'region': region}), encoding='utf8'))

    return "Deletion task has been submitted. This is an asynchronous operation, and will take few seconds to minutes. List the ENI again to see the status."
        
def tohtml2(region, msg):
    return """<html>
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
        <body><div>""" + msg + """</div></body></html>"""

def tohtml(region, enilist):
    sorted_list = sorted(enilist, key=lambda k: k['Status'], reverse=True)
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
        <body>
            <table border=1>
                <tr>
                    <th>ENI Type</th>
                    <th>ENI-Id</th>
                    <th>Function Name</th>
                    <th>Ip-Address</th>
                    <th>Availability Zone</th>
                    <th>Subnet</th>
                    <th>Status</th>
                </tr>
            <indent>"""
    enitype = fnname = ''
    for eni in sorted_list:
        if eni['Status'] == 'available':
            enitype = fnname = 'N/A'
        elif eni['Status'] == 'in-use':
            if eni['Attachment']['AttachmentId'].split("-")[0] == 'ela':
                enitype = 'Hyperplane ENI'
                fnname = 'N/A'
            elif eni['Attachment']['AttachmentId'].split("-")[0] == 'eni':
                enitype = 'VPC ENI'
                fnname = eni['RequesterId'].split(":")[1]
        message += """
                <tr>
                    <td> """ + enitype + """ </td>
                    <td> """ + eni['NetworkInterfaceId'] + """ </td>
                    <td> """ + fnname + """ </td>
                    <td> """ + eni['PrivateIpAddress'] + """ </td>
                    <td> """ + eni['AvailabilityZone'] + """ </td>
                    <td> """ + eni['SubnetId'] + """ </td>
                    <td> """ + eni['Status'] + """ </td>
                </tr>"""
    message += """</indent>
            </table>
        </body></html>"""
    return message

def lambda_handler(event, context):
    region = event['queryStringParameters']['region']
    status = event['queryStringParameters']['status']
    op = event['queryStringParameters']['type']
    #status = 'All' #'All', 'Available' or 'In-use'
    #op = 'Delete' #'List' or 'Delete'
    #region='ap-southeast-2'
    message = listeni(region, op, status, context)
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': { "Content-Type": "text/html"},
        'body': message }