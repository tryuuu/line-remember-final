from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, QuickReplyButton, MessageAction, QuickReply, TextSendMessage, ImageSendMessage)

class QuickReplyManager:
    def __init__(self):
        self.items = [
            QuickReplyButton(action=MessageAction(label='教えて', text='教えて')),
            QuickReplyButton(action=MessageAction(label='忘れて', text='忘れて'))
        ]

    def quick_reply(self, *args):
        messages = []
        for text in args:
            messages.append(TextSendMessage(text=text, quick_reply=QuickReply(items=self.items)))
        return messages

    def quick_reply_with_image(self, image_url):
        return QuickReply(items=self.items)