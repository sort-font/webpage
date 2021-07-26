from PIL import Image
import numpy as np
from keras.models import model_from_json
import pickle, sys

with open("list_row.pkl", "rb") as f:
  list_row = pickle.load(f)


with open("model.model", 'r') as f:
    json_string = f.read()
model = model_from_json(json_string)

model.load_weights('param.hdf5')


def predict_font(img):
  im_resized = np.resize(img, (64, 64, 3)).reshape(1, 64, 64, 3).astype("f")
  pred = model.predict(im_resized)
  
  try:
    font_name = list_row[np.argmax(pred)]
    print(np.argmax(pred))
    idx = font_name.find(".")
    r = font_name[:idx]
  except Exception as e:
    print(e, file=sys.stderr)
    r = None
  
  return r
