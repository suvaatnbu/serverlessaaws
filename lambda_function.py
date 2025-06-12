# This code is intended to run inside AWS Lambda with proper SSL and boto3 support.
# If testing locally or in restricted environments, ensure Python's SSL module is properly installed.

try:
    import boto3
except ImportError as e:
    raise ImportError("boto3 is required to run this function. Make sure it's installed and SSL dependencies are available.") from e

def lambda_handler(event, context):
    try:
        ec2 = boto3.client('ec2',region_name='ap-south-1')

        # Auto-Stop instances
        stop_instances = ec2.describe_instances(
            Filters=[
                {'Name': 'tag:Action', 'Values': ['Auto-Stop']},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
        stop_ids = [i['InstanceId'] for r in stop_instances['Reservations'] for i in r['Instances']]
        if stop_ids:
            ec2.stop_instances(InstanceIds=stop_ids)
            print(f"Stopped instances: {stop_ids}")

        # Auto-Start instances
        start_instances = ec2.describe_instances(
            Filters=[
                {'Name': 'tag:Action', 'Values': ['Auto-Start']},
                {'Name': 'instance-state-name', 'Values': ['stopped']}
            ]
        )
        start_ids = [i['InstanceId'] for r in start_instances['Reservations'] for i in r['Instances']]
        if start_ids:
            ec2.start_instances(InstanceIds=start_ids)
            print(f"Started instances: {start_ids}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Local test stub
if __name__ == '__main__':
    class DummyContext: pass
    dummy_event = {}
    dummy_context = DummyContext()
    lambda_handler(dummy_event, dummy_context)

