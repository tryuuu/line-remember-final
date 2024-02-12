import json
import boto3
import uuid
from datetime import datetime
import os
def putdb(user_id, tag, item):
    dynamodb = boto3.client('dynamodb')
    table = os.environ['DYNAMODB_TABLE_NAME']
    timestamp = datetime.utcnow().isoformat()
    dynamodb.put_item(
        TableName=table,
        Item={
            'user_id': {'S': user_id},
            'timestamp': {'S': timestamp},
            'tags': {'S': tag},
            'elements': {'S': item}
        }
    )

def putanotherdb(user_id, item):
    dynamodb = boto3.client('dynamodb')
    table = "line-knowledge-db"
    try: 
        response = dynamodb.scan(
            TableName=table,
            FilterExpression='user_id = :user_id and #data = :data',
            ExpressionAttributeNames={
                '#data': 'data',  # 'data' 属性名をエスケープ
            },
            ExpressionAttributeValues={
                ':user_id': {'S': user_id},
                ':data': {'S': item}
            }
        )
        print(response)
    except Exception as e:
        print(f"DynamoDBからのデータ取得中にエラーが発生しました!!: {str(e)}")
        return
    try: 
        for i in response['Items']:
            dynamodb.update_item(
                TableName=table,
                Key={
                    'user_id': {'S': i['user_id']['S']},
                    'timestamp': {'S': i['timestamp']['S']}
                },
                UpdateExpression='SET isclassified = :isclassified',
                ExpressionAttributeValues={
                    ':isclassified': {'BOOL': True}
                }
            )
    except Exception as e:
        print(f"DynamoDBへの更新中にエラーが発生しました!: {str(e)}")
        return

def handler(event,context):
    body = json.loads(event['body'])
    print(body)
    user_id = body.get('user_id')
    tag = body.get('tag')
    item = ''
    if 'item' in body:
        item = body.get('item')
        putdb(user_id,tag, item)
        putanotherdb(user_id, item)
    else:
        putdb(user_id,tag, item)
    return {
        'statusCode': 200,
         'body': "success"
    }