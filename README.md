# lambdautilities
AWS Lambda Utilities

Region : N.Virginia (Deployment should be in this region)


I) Lambda Statistcis

This utility can be used to aggregate the lambda function executions in a region based on total invocations,errors,throttles or  duration, and display in a reverse order.

Required Input:

Region: Select the region where you want to look for the lambda aggregates for invocation, errors, throttles or duration.
Metrics : Choose which metric aggregates you want to look for.
Hours : Choose the search length. (Max 24 hours)

Use-cases:

1) Finding highest invoked functions in a region for the last 24 hours, and display in a reverse order.
2) Find the functions which takes highest duration, display in reverse order.
3) Find which functions throttles for the last 24 hours.
4) Find the functions which are erroring out, and its error rate for last 24 hour.

II) Lambda@Edge Logs Finder

This utility helps to find the lambda@Edge function logs stored in different region for the last hours (Max 24 hours). The result includes hyperlink text, and by clicking it, will navigate to that particular lambda@Edge logs.

Required Input:

Function Name : Enter the function name
Hours : Choose the search length. (Max 24 hours)

Use-cases:

1) Finding which region the choosen lambda@Edge function logs is stored, and navigate into that region Cloudwatch log page.

III) Lambda ENIs Find/Delete

This utility helps to find or delete the ENIs created by lambda. ENIs created by lambda is auto deleted by lambda after certain interval, however if you want to delete before that interval, or if the ENIs are not deleted for some reason, you can use this utility to delete.

UPDATE : With the introduction of VPC Improved networking with Lambda, the above is not the case anymore. Lambda will have dedicated ENI (Hyperplane ENI) to use it with VPC lambda functions. And these ENIs cannot be deleted, as these will be in-use for multiple lambda functions. However, you can still list the ENIs, or use this utiility for AWS accounts who have blacklisted for this new feature (That is those AWS accounts which still uses Old VPC networking functionality)

Important:

"Delete" Operation is only supported when selected with "Available" ENIs.

Required Input:

Region: Select the region where you want to look for the lambda ENIs used by lambda
Operation : Choose the operation - "List" or "Delete"
Status : Choose which status ENI should be displayed. If the operation is "Delete" only "Avaialble" status is supported.

Use-cases:

1) Listing the ENIs used by lambda
2) Delete the ENIs used by lambda, if lambda doesnt deleted automatically for some reason. Deletion of ENI is not required for AWS accounts which enabled for "VPC Improved networking for Lambda".



How to Deploy: (Note - Deployment should be in N.Virginia region)

1) Open Lambda Console
2) Navigate to N.Virginia Region
3) Choose - Crete Function
4) Select "Browse serverless app repository"
5) Tick "Show apps that create custom IAM roles or resource policies"
6) Search "LambdaUtilities", and click on it.
7) Click "I acknowledge this app creates custom IAM roles"
8) click "Deploy"

It may take a while to deploy.

How to access the deployed application:

1) On the "Deploy" page, click on "Test app" button once deployment is completed.
2) Click the "API Endpoint" to access the application, on the next page.
3) You have an option to choose the region where you want the choosen operation to be performed.

You can Access the README.md file or any raise any issues at:
https://github.com/neogk666/lambdautilities



