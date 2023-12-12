import json
import boto3
import os

def deletedb(user_id, num):
    dynamodb = boto3.client('dynamodb')
    table = os.environ['DYNAMODB_TABLE_NAME']

    try:
        response = dynamodb.query(
            TableName=table,
            KeyConditionExpression='user_id = :user_id',
            ExpressionAttributeValues={':user_id': {'S': user_id}},
            ScanIndexForward=True
        )
        items = response.get('Items', [])
    except Exception as e:
        print(f"DynamoDBからのデータ取得中にエラーが発生しました: {str(e)}")
        return

    if num <= len(items):
        item_to_delete = items[num - 1]
        dynamodb.delete_item(
                TableName=table,
                Key={
                    'user_id': {'S': item_to_delete['user_id']['S']},
                    'timestamp': {'S': item_to_delete['timestamp']['S']}
                }
            )
    else:
        print("存在しません")
        
def handler(event,context):
    body = json.loads(event['body'])
    print(body)
    num = body.get('index')
    print(num)
    user_id = body.get('user_id')
    deletedb(user_id,num)
    return {
        'statusCode': 200,
         'body': "success"
    }