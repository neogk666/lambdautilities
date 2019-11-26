# lambdautilities
AWS Lambda Utilities

Region : N.Virginia

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
Metrics : Choose which metric aggregates you want to look for.
Hours : Choose the search length. (Max 24 hours)
