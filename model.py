from PIL import Image
import numpy as np
from keras.models import model_from_json
import pickle, sys, traceback

class FontData:
  def __init__(self, name, probability) -> None:
    self.name = name
    self.probability = probability

with open("list_row.pkl", "rb") as f:
  list_row = pickle.load(f)

  # .以降は起動時に消しておけば、判定時間の短縮につながりそう
  for idx, name in enumerate(list_row):
    list_row[idx] = list_row[idx][:list_row[idx].find(".")]

with open("model.model", 'r') as f:
    json_string = f.read()
model = model_from_json(json_string)

model.load_weights('param.hdf5')

def predict_font(img, display_num : int = 1):
  IMG_SIZE = (64, 64, 3)
  im_resized = np.resize(img, IMG_SIZE).reshape(1, 64, 64, 3).astype("f")
  pred = model.predict(im_resized)
  
  try:
    # 降順にソートして、前からdisplay_num分取得する
    idxs = np.argsort(-pred[0])[:display_num]
    r = [FontData(list_row[idx], pred[0][idx]) for idx in idxs if idx < len(list_row)]
  except Exception as e:
    print(e, file=sys.stderr)
    print(traceback.format_exc())
    r = None
  
  return r
