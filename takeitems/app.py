import json
import boto3
import os
def takeitems(user_id, tag):
    dynamodb = boto3.client('dynamodb')
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    try: 
        response = dynamodb.query(  
            TableName=table_name,
            KeyConditionExpression='user_id = :user_id',
            ExpressionAttributeValues={
                ':user_id': {'S': user_id}
            }
        )
        print(response) 
    except Exception as e:
        print(f"DynamoDBからのデータ取得中にエラーが発生しました: {str(e)}")
        return
    items = response.get('Items', [])
    return items

def handler(event,context):
    body = json.loads(event['body'])
    print(body)
    user_id = body.get('user_id')
    tag = body.get('tag')
    items = takeitems(user_id, tag)
    result = []
    for item in items:
        if item['tags']['S'] == tag and item['elements']['S'] != '':
            result.append(item['elements']['S'])
    print(result)
    return {
        'statusCode': 200,
         'body': json.dumps(result)
    }