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

def handler(event, context):
    body = json.loads(event['body'])
    events = body['events']
    user_id = events[0]['source']['userId']
    reply_token = events[0]['replyToken']  
    format = events[0]['message']['type']
    print(f"フォーマット:{format}")
    
    if format == "image":
        message_id = events[0]['message']['id']
        image_content = line_bot_api.get_message_content(message_id)
        image_data = image_content.content
        file_path = upload_to_s3(image_data,user_id)
        savedb_manager.save_to_db(user_id,file_path)
        text = "写真を覚えたよ！"
        messages = quickreply_manager.quick_reply(text)
        line_bot_api.reply_message(reply_token,messages=messages)
        return {
            'statusCode': 200,
            'body': json.dumps('Error: Non-text message received')
        }

    if format != "text":
        error_message = "すみません、テキストメッセージ以外のメッセージは受け付けていません。再度回答をお願いします。"
        messages = quickreply_manager.quick_reply(error_message)
        line_bot_api.reply_message(reply_token,messages=messages)
        return {
            'statusCode': 200,
            'body': json.dumps('Error: Non-text message received')
        }
    content = events[0]['message']['text']
    try:
        if content == "教えて" or content == "おしえて":
                db_data = getdb_manager.get_from_db(user_id)
                print(db_data)
                n = len(db_data)
                i = random.randint(0,n-1)
                print(db_data[i]['data'])
                knowledge = db_data[i]['data']['S']
                savedb_manager.save_to_db2(user_id,knowledge)
                # データがURLの場合（画像）
                if knowledge.startswith('https://'):
                    # 画像メッセージを作成して送信
                    quick_reply = quickreply_manager.quick_reply_with_image(knowledge)
                    image_message = ImageSendMessage(original_content_url=knowledge, preview_image_url=knowledge, quick_reply=quick_reply)
                    line_bot_api.reply_message(reply_token, image_message)
                else:
                    messages = quickreply_manager.quick_reply(knowledge)
                    line_bot_api.reply_message(reply_token,messages=messages)
        elif content == "忘れて" or content == "わすれて" or content == "忘れる" or content == "わすれる":
            former_data = getdb_manager.get_from_db2(user_id)
            print(former_data)
            delete_from_db(user_id,former_data)
            if former_data.startswith('https://'):
                text = "その写真を忘れたよ！"
            else:
                text = f"「{former_data}」を忘れたよ！"
            messages = quickreply_manager.quick_reply(text)
            line_bot_api.reply_message(reply_token,messages=messages)
        else:
            savedb_manager.save_to_db(user_id,content)
            savedb_manager.save_to_db2(user_id,content)
            text = f"「{content}」だね！覚えたよ！"
            messages = quickreply_manager.quick_reply(text)
            line_bot_api.reply_message(reply_token,messages=messages)
    except Exception as e:
        text = "エラーが発生しました。"
        messages = quickreply_manager.quick_reply(text)
        line_bot_api.reply_message(reply_token,messages=messages)
    return {
            'statusCode': 200,
            'body': json.dumps('Error: Non-text message received')
        }