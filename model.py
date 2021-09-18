import numpy as np
from keras.models import model_from_json
import pickle
import sys
import traceback
from tensorflow.keras import models


class FontData:
    def __init__(self, name, probability) -> None:
        self.name = name
        self.probability = probability


with open("model/font_list.pkl", "rb") as f:
    list_row = pickle.load(f)

    # .以降は起動時に消しておけば、判定時間の短縮につながりそう
    for idx, name in enumerate(list_row):
        list_row[idx] = list_row[idx][:list_row[idx].find(".")]

with open("model/alex_net/model.json", 'r') as f:
    json_string = f.read()
model = model_from_json(json_string)

model.load_weights('model/alex_net/param.hdf5')

model_google = models.load_model('model/google_net')
model_google.load_weights('model/google_net')


def predict_font(img, display_num: int = 1):
    # alexNetの推論
    im_resized = img.reshape(1, 64, 64, 3).astype("f")
    pred_1 = model.predict(im_resized)
    # GoogleNetの推論
    im_resized_norm = im_resized / 255
    pred_2 = model_google.predict(im_resized_norm)
    # 1:1でアンサンブル
    pred = (pred_1 + pred_2)/2

    try:
        # 降順にソートして、前からdisplay_num分取得する
        idxs = np.argsort(-pred[0])[:display_num]
        r = [FontData(list_row[idx], pred[0][idx])
            for idx in idxs if idx < len(list_row)]
    except Exception as e:
        print(e, file=sys.stderr)
        print(traceback.format_exc())
        r = None

    return r
