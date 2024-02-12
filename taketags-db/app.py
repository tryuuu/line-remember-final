import json
import boto3
import os
def taketags(user_id):
    dynamodb = boto3.client('dynamodb')
    table = os.environ['DYNAMODB_TABLE_NAME']
    response = dynamodb.query(
        TableName=table,
        KeyConditionExpression='user_id = :user_id',
        ExpressionAttributeValues={
            ':user_id': {'S': user_id}
        }
    )
    items = response.get('Items', [])
    return items

def handler(event,context):
    body = json.loads(event['body'])
    print(body)
    user_id = body.get('user_id')
    tags = []
    items = taketags(user_id)
    for item in items:
        if item['elements']['S'] == '':
            tags.append(item['tags']['S'])
    print(tags)
    return {
        'statusCode': 200,
         'body': json.dumps(tags)
    }