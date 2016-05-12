import json

import requests

from app.settings import TOKEN

TELEGRAM_URL_API = 'https://api.telegram.org/bot'


def __build_url(method):
    url = '{}{}/{}'.format(TELEGRAM_URL_API, TOKEN, method)
    return url


def __post(url, body, params=dict()):
    """
    Internal post
    :param url:
    :param body:
    :param params:
    :return:
    """
    try:
        headers = {'Content-type': 'application/json'}
        requests.post(url, data=body, params=params, headers=headers)
    except Exception as e:
        print(e)


def send_message(message):
    """
    It sends a message to telegram
    :param message: dict() whith "text" mandatory
    :return:
    """
    method = 'sendMessage'
    url = __build_url(method)
    __post(url, json.dumps(message))
