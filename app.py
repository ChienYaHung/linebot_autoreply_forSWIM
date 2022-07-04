from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, PostbackEvent,
                            TextSendMessage, TemplateSendMessage,
                            ConfirmTemplate, MessageTemplateAction,
                            ButtonsTemplate, PostbackTemplateAction,
                            URITemplateAction, CarouselTemplate,
                            CarouselColumn, ImageCarouselTemplate,
                            ImageCarouselColumn)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'd3XBa+e/nxMu6KhzQPgDMt9uK1nBw+hQUEVXhXD1zL/KgM6quFVLT7zqOYd++xVlMIHVHtwMdmAfMIieacnaFtr1tb0U7G30M67SSi0C5wlhC7vEWivNKZCqHRLcIhvJw6L5V81MiV/3J2dGQt5E8wdB04t89/1O/w1cDnyilFU='
)
handler = WebhookHandler('0a39f8e33a87caba5a0511b1648d0526')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)  #收到訊息時觸發以下函式
def handle_message(event):
    mtext = event.message.text  #接收到的訊息
    if mtext == "@各店資訊":
        sendButton(event)


def sendButton(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/rBpJL3U.jpg',  #顯示的圖片
                title='北區文賢店',  #主標題
                text='704台南市北區文賢路795號',  #副標題
                actions=[
                    URITemplateAction(  #開啟文賢店google地圖
                        label='Google地圖',
                        uri='https://goo.gl/maps/sy7QmR8BaWeaA5qE7'),
                    MessageTemplateAction(  #文賢店營業時間
                        label='營業時間', text='@營業時間'),
                    URITemplateAction(  #文賢店電話，按下後可撥號
                        label='連絡電話', uri='tel:+886-6-2598198')
                ]),
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='發生錯誤！'))


if __name__ == "__main__":
    app.run()