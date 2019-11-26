def form(url):
    return """<html>
        <head><style type="text/css">
        body {background-color: lightgoldenrodyellow;}
            form {
                text-align: center;
                font-size: 18px;
                font-family: sans-serif;
                color:#ed3330;}
            br.one {
                line-height: 42px;}
            select {
                display:inline-block;
                text-align-last:center;
                text-align:center;
                font-size: 14px;
                font-family: sans-serif;
                font-weight: 700;
                color: #444;
                padding: .6em 1.4em .5em .8em;
                width: 75%;
                box-sizing: border-box;
                border: 1px solid #aaa;
                box-shadow: 0 1px 0 1px rgba(0,0,0,.04);
                border-radius: .5em;
                -moz-appearance: none;
                -webkit-appearance: none;
                background-color: #aaa;}
            input.hidden {
                text-align:center;
                font-size: 14px;
                font-family: sans-serif;
                font-weight: 700;
                color: lightgoldenrodyellow;;
                padding: .6em 1.4em .5em .8em;
                width: 75%;
                box-sizing: border-box;
                border: 1px solid lightgoldenrodyellow;
                border-radius: .5em;
                -moz-appearance: none;
                -webkit-appearance: none;
                background-color: lightgoldenrodyellow;}
            input.noselect {
                text-align:center;
                font-size: 14px;
                font-family: sans-serif;
                font-weight: 700;
                color: #444;
                padding: .6em 1.4em .5em .8em;
                width: 75%;
                box-sizing: border-box;
                border: 1px solid #aaa;
                box-shadow: 0 1px 0 1px rgba(0,0,0,.04);
                border-radius: .5em;
                -moz-appearance: none;
                -webkit-appearance: none;
                background-color: #aaa;}
            input.addtext {
                text-align:center;
                font-size: 14px;
                font-family: sans-serif;
                font-weight: 700;
                color: #444;
                padding: .6em 1.4em .5em .8em;
                width: 75%;
                box-sizing: border-box;
                border: 1px solid #aaa;
                box-shadow: 0 1px 0 1px rgba(0,0,0,.04);
                border-radius: .5em;
                -moz-appearance: none;
                -webkit-appearance: none;
                background-color: #aaa;}
            table {
                border: 0px solid black;
                border-spacing: 20px;
            }
            td {
                border: 1px solid black;}
            th {
                text-align: center;
                font-size: 18px;
                font-family: sans-serif;
                color:#ed3330;}
            input[type=submit] {
                color: #fff !important;
                font-family: sans-serif;
                text-transform: uppercase;
                text-decoration: none;
                background: #ed3330;
                padding: 20px;
                border-radius: 5px;
                display: inline-block;
                border: none;
                transition: all 0.4s ease 0s;}
            input[type=submit]:hover {
                background: #434343;
                font-family: sans-serif;
                letter-spacing: 1px;
                -webkit-box-shadow: 0px 5px 40px -10px rgba(0,0,0,0.57);
                -moz-box-shadow: 0px 5px 40px -10px rgba(0,0,0,0.57);
                box-shadow: 5px 40px -10px rgba(0,0,0,0.57);
                transition: all 0.4s ease 0s;}
        </style></head>
        <body>
            <table>
            <tr><th style="width:250px;height:50px">Lambda Statistics</th>
            <th style="width:250px;height:50px">Lambda@Edge Logs Finder</th>
            <th style="width:250px;height:50px">Lambda ENIs Find/Delete</th></tr>
            <tr><td style="height:250px">
            <form action='""" + url + """/find'><br>
            Region<br>
            <select name="region" size="1">
                <option value="us-east-1" selected>N. Virginia</option>
                <option value="us-east-2">Ohio</option>
                <option value="us-west-1">N. California</option>
                <option value="us-west-2">Oregon</option>
                <option value="ap-east-1">Hong Kong</option>
                <option value="ap-south-1">Mumbai</option>
                <option value="ap-northeast-2">Seoul</option>
                <option value="ap-southeast-1">Singapore</option>
                <option value="ap-southeast-2">Sydney</option>
                <option value="ap-northeast-1">Tokyo</option>
                <option value="ca-central-1">Canada</option>
                <option value="eu-central-1">Frankfurt</option>
                <option value="eu-west-1">Ireland</option>
                <option value="eu-west-2">London</option>
                <option value="eu-west-3">Paris</option>
                <option value="eu-north-1">Stockholm</option>
                <option value="sa-east-1">Sao Paulo</option>
                <option value="me-south-1">Bahrain</option>
            </select><br><br>
            Metrics<br>
            <select name="type" size="1">
                <option value="Invocations" selected>Invocations</option>
                <option value="Errors">Errors</option>
                <option value="Throttles">Throttles</option>
                <option value="Duration">Duration</option>
            </select><br><br>
            Hours<br>
            <select name="hours" size="1">
                <option value="1" selected>1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="6">6</option>
                <option value="12">12</option>
                <option value="18">18</option>
                <option value="24">24</option>
            </select><br><br><br>
            <input type="submit" value="Submit">
            </form>
            </td>
            <td style="height:250px">
            <form action='""" + url + """/edgelogs'><br>
            Region<br>
            <input type="text" name="region" value="N. Virginia" class="noselect" disabled="disabled"/><br><br>
            Function Name<br>
            <input type="text" name="function" class="addtext"/><br><br>
            Hours<br>
            <select name="hours" size="1">
                <option value="1" selected>1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="6">6</option>
                <option value="12">12</option>
                <option value="18">18</option>
                <option value="24">24</option>
            </select><br><br><br>
            <input type="submit" value="Submit">
            </form>
            </td><td style="height:250px">
            <form action='""" + url + """/listeni'><br>
            Region<br>
            <select name="region" size="1">
                <option value="us-east-1" selected>N. Virginia</option>
                <option value="us-east-2">Ohio</option>
                <option value="us-west-1">N. California</option>
                <option value="us-west-2">Oregon</option>
                <option value="ap-east-1">Hong Kong</option>
                <option value="ap-south-1">Mumbai</option>
                <option value="ap-northeast-2">Seoul</option>
                <option value="ap-southeast-1">Singapore</option>
                <option value="ap-southeast-2">Sydney</option>
                <option value="ap-northeast-1">Tokyo</option>
                <option value="ca-central-1">Canada</option>
                <option value="eu-central-1">Frankfurt</option>
                <option value="eu-west-1">Ireland</option>
                <option value="eu-west-2">London</option>
                <option value="eu-west-3">Paris</option>
                <option value="eu-north-1">Stockholm</option>
                <option value="sa-east-1">Sao Paulo</option>
                <option value="me-south-1">Bahrain</option>
            </select><br><br>
            Operation<br>
            <select name="type" size="1">
                <option value="List" selected>List</option>
                <option value="Delete">Delete</option>
            </select><br><br>
            Status<br>
            <select name="status" size="1">
                <option value="All" selected>All</option>
                <option value="Available">Available</option>
                <option value="In-use">In-use</option>
            </select><br><br><br>
            <input type="submit" value="Submit">
            </form>
            </td></tr>
            </table>
        </body>
    </html>"""

def lambda_handler(event, context):
    url = 'https://' + event['requestContext']['domainName'] + '/' + event['requestContext']['stage']
    message = form(url)
    return {
    'isBase64Encoded': False,
    'statusCode': 200,
    'headers': { "Content-Type": "text/html"},
    'body': message }