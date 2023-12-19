import json
import os
import random
from src.database import SaveDBManager,GetDBManager,delete_from_db
from src.quickreply import QuickReplyManager
from src.s3 import upload_to_s3
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, QuickReplyButton, MessageAction, QuickReply, TextSendMessage, ImageSendMessage)
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
line_bot_api = LineBotApi(channel_access_token)

savedb_manager = SaveDBManager()
getdb_manager = GetDBManager()
quickreply_manager = QuickReplyManager()

def handler(event,context):
    user_ids = getdb_manager.get_all_user()
    for user_id in user_ids:
        db_data = getdb_manager.get_from_db(user_id)
        print(db_data)
        n = len(db_data)
        i = random.randint(0,n-1)
        print(db_data[i]['data'])
        knowledge = db_data[i]['data']['S']
        savedb_manager.save_to_db2(user_id,knowledge)
        # データがURLの場合（画像）
        if knowledge.startswith('https://line-knowledge-ryu'):
            # 画像メッセージを作成して送信
            quick_reply = quickreply_manager.quick_reply_with_image(knowledge)
            image_message = ImageSendMessage(original_content_url=knowledge, preview_image_url=knowledge, quick_reply=quick_reply)
            line_bot_api.push_message(user_id, image_message)
        else:
            messages = quickreply_manager.quick_reply(knowledge)
            line_bot_api.push_message(user_id,messages=messages)
        return {
        'statusCode': 200,
         'body': "success"
    }