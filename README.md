# AWS EC2 Auto Start/Stop using Lambda

## ✅ Description
This project automates the **start** and **stop** of EC2 instances based on tags using AWS Lambda and Boto3.

## ✅ Tags Used
- `Auto-Start`: `true`
- `Auto-Stop`: `true`

## ✅ Lambda Permissions
IAM Role:
- `ec2:DescribeInstances`
- `ec2:StartInstances`
- `ec2:StopInstances`

## ✅ Steps Followed

1. Created a Lambda function with Python 3.x runtime
2. Attached necessary IAM permissions
3. Created CloudWatch Event Rule for scheduling
4. Tested with tagged EC2 instances

## ✅ Sample Code

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Auto-Start
    start_instances = ec2.describe_instances(
        Filters=[{'Name': 'tag:Auto-Start', 'Values': ['true']}]
    )
    for reservation in start_instances['Reservations']:
        for instance in reservation['Instances']:
            ec2.start_instances(InstanceIds=[instance['InstanceId']])
    
    # Auto-Stop
    stop_instances = ec2.describe_instances(
        Filters=[{'Name': 'tag:Auto-Stop', 'Values': ['true']}]
    )
    for reservation in stop_instances['Reservations']:
        for instance in reservation['Instances']:
            ec2.stop_instances(InstanceIds=[instance['InstanceId']])

