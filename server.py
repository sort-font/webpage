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
import random
from io import BytesIO
from PIL import Image
from datetime import date

app = Flask(__name__, static_url_path="/static")


class FontsDataResponse:
    def __init__(self, fonts_data: model.FontData, message: str = "") -> None:
        # font_dataが空ならOKではない
        self.ok = fonts_data != None
        self.fonts_data = fonts_data
        self.message = message

class EvalResponse:
    def __init__(self, enter: str, judge: str, func: str) -> None:
        self.enter = enter
        self.judge = judge
        self.func = func

SAVE_DIR = "./static/images"
# ディレクトリがなかったら作成するコードを追加
try:
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
except Exception as e:
    print(e)

img = 0
is_gray_scale = 0

@app.route('/')
def index():
    """
    過去の判定画像をランダムに PREVIEW_NUM 件返す関数
    """

    # queryで表示数を変更することもできる実装にしておいた
    PREVIEW_NUM = 12
    return render_template('index.html',
                           images=random.choices(os.listdir(SAVE_DIR), k=PREVIEW_NUM))

# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b


@app.route("/crop_image", methods=["POST"])
def crop_image():
    """
    切り抜いたフォントを取得する関数
    """
    global img
    global is_gray_scale
    try:
        if request.method == "POST":
            # 画像として読み込み
            enc_data = request.form.getlist('croped_image')
            dec_data = base64.b64decode(enc_data[0].split(',')[1])
            img_np = np.frombuffer(dec_data, np.uint8)
            img = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)

            img_resized = Image.fromarray(img).resize((64, 64))
            img = np.array(img_resized)
            is_gray_scale = request.form.getlist('is_gray_scale')[0]
            if is_gray_scale == "1":
                gray_img = Image.fromarray(img).convert("L")
                img = np.array(gray_img)
                img = np.concatenate([img, img, img], axis=0)

            return render_template('index.html')

    except Exception as e:
        print("error")
        print(e, file=sys.stderr)
        print(traceback.format_exc())
        return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """
    ユーザから受け取った画像を用いて、フォントの判定を行う関数
    """
    global img
    try:
        if request.files == None:
            return render_template('result.html', font_data_response=FontsDataResponse(None, "ファイルがアップロードされていません"))
        else:
            display_num = 5
            display_num_str = request.form["display_num"]
            if len(display_num_str) > 0 and int(display_num_str) > 0:
                display_num = int(display_num_str)

            fonts_data = model.predict_font(img, display_num)

            if fonts_data == None:
                return render_template('result.html', fonts_data_response=FontsDataResponse(None, '該当するフォントがありませんでした'))

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
    enter = request.form.get('enter')
    judge = request.form.get('judge')
    func = request.form.get('func')
    if os.path.exists('enter.txt'):
        with open("enter.txt", "a", encoding="utf-8") as f:
            f.write(f"\n\n{str(date.today())}\n{enter}, {judge}, {func}")
    else:
        with open("enter.txt", "w", encoding="utf-8") as f:
            f.write(f"\n\n{str(date.today())}\n{enter}, {judge}, {func}")
    return render_template('enter.html', eval=EvalResponse(enter, judge, func))


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
