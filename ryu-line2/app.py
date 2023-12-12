import json
import os
from src.database import GetDBManager,deletedb
getdb_manager = GetDBManager()

def handler(event,context):
    result = []
    body = json.loads(event['body'])
    user_id = body['user_id']
    print(user_id)
    items = getdb_manager.get_from_db(user_id)
    for item in items:
        item.pop('id', None)
        item.pop('user_id', None)
    for item in items:
        result.append(item['data']['S'])

    print(items)
    return {
        'statusCode': 200,
         'body': json.dumps(result)
    }
