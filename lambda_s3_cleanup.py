import boto3
import datetime

def lambda_handler(event, context):
    bucket_name = 'your-bucket-name'  # Replace with your S3 bucket name
    days_threshold = 30

    s3 = boto3.client('s3')
    deleted_files = []

    # Get today's date
    today = datetime.datetime.now(datetime.timezone.utc)

    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        for obj in response['Contents']:
            last_modified = obj['LastModified']
            age = (today - last_modified).days

            if age > days_threshold:
                print(f"Deleting {obj['Key']} (Last Modified: {last_modified})")
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                deleted_files.append(obj['Key'])
    
    return {
        'statusCode': 200,
        'body': f"Deleted {len(deleted_files)} files: {deleted_files}"
    }

