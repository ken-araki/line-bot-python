from django.shortcuts import render
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent, TextMessage, TextSendMessage,
)
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

line_bot_api = LineBotApi(getattr(settings, "LINE_BOT_CHANNEL_TOKEN", None))
handler = WebhookHandler(getattr(settings, "LINE_BOT_CHANNEL_SECRET", None))

# Create your views here.
@csrf_exempt
def callback(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        HttpResponseForbidden()

    return HttpResponse('OK', status=200)

@handler.add(MessageEvent, message=TextMessage)
def handleTextEventMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(FollowEvent)
def handleFollowEventMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Hello World!'))