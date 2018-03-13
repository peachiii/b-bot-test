# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/')
def index():
    return 'bee reply'
@app.route('/bot', methods=['POST'])

def bot():
    host_to_sent = '{userId of host}'
    # ข้อความที่ต้องการส่งกลับ
    replyStack = list()

    # ข้อความที่ได้รับมา
    msg_in_json = request.get_json()
    msg_in_string = json.dumps(msg_in_json)

    # Token สำหรับตอบกลับ (จำเป็นต้องใช้ในการตอบกลับ)
    replyToken = msg_in_json["events"][0]['replyToken']

    userID = msg_in_json["events"][0]['source']['userId']
    msgType = msg_in_json["events"][0]['message']['type']


    if msgType != 'text':
        reply(replyToken,msg_in_json["events"])
        # reply(replyToken, ['Only text is allowed.'])
        return 'OK', 200

    text = msg_in_json["events"][0]['message']['text'].lower().strip()

    if '{' in host_to_sent:
        replyStack.append("userId: %s" % userID)
        host_to_sent = userID
    else:
        try:
            replyStack.append("%s said %s" % (getProfileUser(msg_in_json["events"][0]['source']['userId']).json()['displayName'],text))
        except:
            replyStack.append('error to get displayName')

    push(host_to_sent,replyStack[:5])
    return 'OK', 200



def push(userid,textList):
    LINE_API = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': LINE_API_KEY
    }
    msgs = []
    for text in textList:
        msgs.append({
            "type": "text",
            "text": text
        })
    data = json.dumps({
        "to": userid,
        "messages": msgs
    })
    requests.post(LINE_API, headers=headers, data=data)
    return

def getProfileUser(userid):

    LINE_API = 'https://api.line.me/v2/bot/profile/%s' % userid
    headers = {
        'Authorization': LINE_API_KEY
    }
    data = requests.get(LINE_API, headers=headers)
    return data


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')