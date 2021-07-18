# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, url_for
import numpy as np
import cv2
import os
import model
import uuid


app = Flask(__name__, static_url_path="/static")


SAVE_DIR = "./static/images"


@app.route('/')
def index():
    return render_template('index.html', images=os.listdir(SAVE_DIR)[::-1])

# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b
@app.route('/upload', methods=['POST'])
def upload():
    if request.files['image']:
        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)
        font_name = model.predict_font(img)

        if font_name == None:
            return render_template('result.html', fontName='"エラーが起きてしまって、フォントを特定できませんでした、、申し訳ない。')
        
        cv2.imwrite(os.path.join(SAVE_DIR, font_name + '_' + str(uuid.uuid4()) + '.png'), img)
        return render_template('result.html', fontName=font_name)

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
    app.run(host='0.0.0.0', port=8888)
