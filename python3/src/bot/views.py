from django.shortcuts import render
from django.http import HttpResponse
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

from google.cloud import translate
from bot.models import Translation_length
import datetime

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
    now = datetime.datetime.now()
    year_month = now.strftime('%Y%m')
    try:
        translation = Translation_length.objects.get(year_month=year_month)
    except Person.DoesNotExist:
        translation = Translation_length(year_month=year_month, translation_length=0)
    translation.translation_length += len(event.message.text)
    translation.update_or_create()
    if translation.translation_length > 500000:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='sorry... Translation processing cannot be performed because the monthly usage limit has been exceeded.'))
        return
    
    translated_text = translate_text(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=translated_text))

@handler.add(FollowEvent)
def handleFollowEventMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Hello World!'))

def translate_text(text):
    """
    Translating Text

    Args:
      text The content to translate in string format
      target_language Required. The BCP-47 language code to use for translation.
    """

    client = translate.TranslationServiceClient()
    project_id = getattr(settings, "GCP_PROJECT_ID", None)

    # TODO(developer): Uncomment and set the following variables
    # text = 'Text you wish to translate'
    # target_language = 'fr'
    # project_id = '[Google Cloud Project ID]'
    contents = [text]
    parent = client.location_path(project_id, "global")

    response = client.translate_text(
        parent=parent,
        contents=contents,
        mime_type='text/plain',  # mime types: text/plain, text/html
        source_language_code='ja',
        target_language_code='en')
    # Display the translation for each input text provided
    for translation in response.translations:
        print(u"Translated text: {}".format(translation.translated_text))
        result = translation.translated_text
    return result
