# -*- coding: utf-8 -*-

import re
from typing import Any
from flask import Flask, render_template, request, url_for
import numpy as np
import cv2
import os
import sys
import uuid
import traceback
import model
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__, static_url_path="/static")


class FontsDataResponse:
  def __init__(self, fonts_data: model.FontData, message: str = "") -> None:
    # font_dataが空ならOKではない
    self.ok = fonts_data != None
    self.fonts_data = fonts_data
    self.message = message


SAVE_DIR = "./static/images"
# ディレクトリがなかったら作成するコードを追加
try:
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
except Exception as e:
    print(e)

img=0

@app.route('/')
def top():
    return render_template('top.html')


@app.route('/index')
def index():
    return render_template('index.html', images=os.listdir(SAVE_DIR)[::-1])


# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b

@app.route("/crop_image", methods=["POST"])
def crop_image():
    global img
    try:
        if request.method=="POST":
            # 画像として読み込み
            enc_data = request.form.getlist('croped_image')
            dec_data = base64.b64decode(enc_data[0].split(',')[1])
            img_np = np.frombuffer(dec_data, np.uint8)
            img = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)
            return render_template('index.html')

    except Exception as e:
        print("error")
        print(e, file=sys.stderr)
        print(traceback.format_exc())
        return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global img
    try:
        if request.files == None:
            return render_template('result.html', font_data_response=FontsDataResponse(None, "ファイルがアップロードされていません"))
        else :
            display_num = 5
            display_num_str = request.form["display_num"]
            if len(display_num_str) > 0 and int(display_num_str) > 0:
                display_num = int(display_num_str)

            fonts_data = model.predict_font(img, display_num)

            if fonts_data == None:
                return render_template('result.html', fonts_data_response=FontsDataResponse(None, 'エラーが起きてしまって、フォントを特定できませんでした、、申し訳ない。'))

            # ファイル名の先頭で最も確率の高かったフォント名を保持しておく
            cv2.imwrite(os.path.join(
                SAVE_DIR, fonts_data[0].name + '_' + str(uuid.uuid4()) + '.png'), img)
            return render_template('result.html', fonts_data_response=FontsDataResponse(fonts_data))
    
    except Exception as e:
        print("error")
        print(e, file=sys.stderr)
        print(traceback.format_exc())
        return render_template('result.html', fonts_data_response=FontsDataResponse(None, '内部的なエラーが発生しました'))

@app.route('/enter', methods=['POST'])
def enter():
    username = request.form.get('username')
    email = request.form.get('email')
    enter = request.form.get('enter')
    with open("enter.txt", "w",encoding="utf=8") as f:
        f.write(username + "\n" + email + "\n" + enter)
    return render_template('enter.html', username=username, email=email, enter=enter)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 8888))
