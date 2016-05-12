from app import application
import json
from flask import render_template, request
from app.monkeynote import monkeybrain
from app.model import cache
from app.settings import mongodb


@application.route("/")
@application.route("/index")
def index():
    return render_template('index.html')


@application.route("/update", methods=['POST'])
def update():
    try:
        body = request.get_json()
        if body:
            update_id = int(body['update_id'])
            last = cache.get_last_message_id(mongodb)
            if update_id > last:
                text = body['message']['text']
                chat_id = body['message']['chat']['id']
                monkeybrain.execute(text, chat_id)
                cache.set_last_message_id(mongodb, update_id)
    except Exception as e:
        print("Exception: {}".format(e))
    return json.dumps({"ok": True})
