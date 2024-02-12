import json
import boto3
import os
#user_idがパーティションキー、tagsがソートキーのテーブルから該当のuser_idとtagを削除する
def deletetag(user_id, tag):
    try:
        dynamodb = boto3.client('dynamodb')
        table = os.environ['DYNAMODB_TABLE_NAME']
        dynamodb.delete_item(
            TableName=table,
            Key={
                'user_id': {'S': user_id},
                'tags': {'S': tag}
            }
        )
        print("削除しました")
    except Exception as e:
        print(f"DynamoDBからのデータ削除中にエラーが発生しました: {str(e)}")
    return

def handler(event,context):
    body = json.loads(event['body'])
    print(body)
    user_id = body.get('user_id')
    tag = body.get('tag')
    deletetag(user_id,tag)
    return {
        'statusCode': 200,
         'body': "success"
    }