import boto3
import os
class GetDBManager:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb')
        self.table_name = os.environ['DYNAMODB_TABLE_NAME']
    
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