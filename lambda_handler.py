import json
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('events')
def lambda_handler(event, context):
    Event_time=event.get('time')
    Event_Source=event.get('source')
    Event_Name=event.get('detail-type')
    Resource_name=event.get('detail').get('instance-id')
    aws_region=event.get('region')
    username=event.get('account') 
    try:
        response = table.put_item(
            Item={
                'Event time': Event_time,
                'Event_Source': Event_Source,
                'Event_Name': Event_Name,
                'Resource_name': Resource_name,
                'aws_region': aws_region,
                'username': username
            }
        )
        print("PutItem succeeded:", json.dumps(response, indent=4))
    except Exception as e:
        print("Error putting item:", e)