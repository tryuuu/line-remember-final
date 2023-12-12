import boto3
import os
import uuid
from datetime import datetime

class SaveDBManager:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb')
        self.table_name = os.environ['DYNAMODB_TABLE_NAME']
        self.table_name2 = os.environ['DYNAMODB_TABLE_NAME2']

    def save_to_db(self, user_id, data):
        try:
            unique_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat()
            
            self.dynamodb.put_item(
                    TableName=self.table_name,
                    Item={
                        'id': {'S': unique_id},
                        'user_id': {'S': user_id},
                        'data': {'S': data},
                        'timestamp': {'S': timestamp}  
                    }
                )
            print(f"User {user_id} のContentをDynamoDBに保存しました。")
        except Exception as e:
            print(f"DynamoDBへの保存中にエラーが発生しました: {str(e)}")
    
    def save_to_db2(self, user, content):
        try:
            self.dynamodb.put_item(
                TableName=self.table_name2,
                Item={
                    'user': {'S': user},
                    'content': {'S': content}
                }
            )
            print("保存成功")
        except Exception as e:
            print(f"保存失敗: {str(e)}")

class GetDBManager:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb')
        self.table_name = os.environ['DYNAMODB_TABLE_NAME']
        self.table_name2 = os.environ['DYNAMODB_TABLE_NAME2']
    
    def get_from_db(self, user_id):
        try:
            response = self.dynamodb.query(
                TableName=self.table_name,
                KeyConditionExpression='user_id = :user_id',
                ExpressionAttributeValues={':user_id': {'S': user_id}},
                ScanIndexForward=True
            )
            items = response.get('Items', [])
            return items
        except Exception as e:
            print(f"DynamoDBからのデータ取得中にエラーが発生しました: {str(e)}")


    def get_from_db2(self, user):
        try:
            response = self.dynamodb.get_item(
                TableName=self.table_name2, 
                Key={'user': {'S': user}}
            )
            item = response.get('Item')
            if item:
                print(item)
                return item.get('content', {}).get('S')
            else:
                print(f"No item found for user: {user}")
                return None
        except Exception as e:
            print(f"取得失敗: {str(e)}")
            return None
  



def delete_from_db(user_id, data):
    dynamodb = boto3.client('dynamodb')
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    try:
        response = dynamodb.scan(
            TableName=table_name,
            FilterExpression='user_id = :user_id and #d = :data',
            ExpressionAttributeValues={
                ':user_id': {'S': user_id},
                ':data': {'S': data}
            },
            ExpressionAttributeNames={
                '#d': 'data'
            }
        )
        items = response.get('Items', [])

        for item in items:
            dynamodb.delete_item(
                TableName=table_name,
                Key={
                    'user_id': {'S': item['user_id']['S']},
                    'timestamp': {'S': item['timestamp']['S']}
                }
            )
        
        print(f"User {user_id} のData '{data}' をDynamoDBから削除しました。")
    except Exception as e:
        print(f"DynamoDBからの削除中にエラーが発生しました: {str(e)}")

