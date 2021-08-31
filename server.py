# -*- coding: utf-8 -*-

from typing import Any
from flask import Flask, render_template, request, url_for
import numpy as np
import cv2
import os
import sys
import uuid
import traceback
import model

app = Flask(__name__, static_url_path="/static")


class FontsDataResponse:
  def __init__(self, fonts_data: model.FontData, message: str = "") -> None:
    # font_dataが空ならOKではない
    self.ok = fonts_data != None
    self.fonts_data = fonts_data
    self.message = message


SAVE_DIR = "./static/images"

@app.route('/')
def top():
    return render_template('top.html')


@app.route('/index')
def index():
    return render_template('index.html', images=os.listdir(SAVE_DIR)[::-1])

# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b


@app.route('/upload', methods=['POST'])
def upload():
    try:
        if request.files == None:
            return render_template('result.html', font_data_response=FontsDataResponse(None, "ファイルがアップロードされていません"))
        if request.files['image']:
            # 画像として読み込み
            stream = request.files['image'].stream
            img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, 1)

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
        print(e, file=sys.stderr)
        print(traceback.format_exc())
        return render_template('result.html', fonts_data_response=FontsDataResponse(None, '内部的なエラーが発生しました'))


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
