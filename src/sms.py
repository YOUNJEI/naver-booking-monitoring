import base64
import hashlib
import hmac
import json
import time

import requests
import os

g_NAVER_ACC_KEY = os.getenv('NAVER_ACC_KEY')
g_NAVER_SECRET_KEY = os.getenv('NAVER_SECRET_KEY')
g_NAVER_SVC_ID = os.getenv('NAVER_SVC_ID')
g_NAVER_PHONE_NUMBER_FROM = os.getenv('NAVER_PHONE_NUMBER_FROM')

def make_signature(method, url, timestamp):
    space = ' '
    newLine = '\n'
    secret_key = bytes(g_NAVER_SECRET_KEY, 'UTF-8')

    message = method + space + url + newLine + timestamp + newLine + g_NAVER_ACC_KEY
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey


def send_message(message, toPhone):
    url = 'https://sens.apigw.ntruss.com/sms/v2/services/' + g_NAVER_SVC_ID + '/messages'

    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    requestHeader = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': g_NAVER_ACC_KEY,
        'x-ncp-apigw-signature-v2': make_signature('POST', '/sms/v2/services/' + g_NAVER_SVC_ID + '/messages', timestamp)
    }

    requestBody = {
        'type': 'SMS',
        'contentType': 'COMM',
        'countryCode': '82',
        'from': g_NAVER_PHONE_NUMBER_FROM,
        'content': message,
        'messages': [{'to': toPhone}]
    }

    response = requests.post(url, headers=requestHeader, data=json.dumps(requestBody))