from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('0DoaCW4dGiwf478IYC+f31/esrN/lbB9HMdkI7vpZdE9xdLoJlAbCSgHPrNTIw7nJLQ/qbsfN/JPkcM7hGaQkeon6AC7YFwSZd/agZf5FJapx9/tKMrdcWRM89GzjH+DH/fi5nQtluxGSk6/etsMeAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a631ddd608d3ee45df4187e218cdd15e')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = "很抱歉，我看不懂你說甚麼"

    if "給我貼圖" in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
        return

    if msg in ["hi", "HI", "hI", "Hi"]:
        r = "嗨"
    elif msg == "你吃飯了嗎":
        r = "還沒"
    elif msg == "你是誰":
        r = "我是機器人"
    elif "訂位" in msg:
        r = "你想訂位，是嘛?"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()