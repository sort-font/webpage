from PIL import Image
import numpy as np
from keras.models import model_from_json
import pickle

list_row = None
with open("list_row.txt", "rb") as f:
  list_row = pickle.load(f)

with open("model_400_epochs.model", 'r') as f:
    json_string = f.read()
model = model_from_json(json_string)

model.load_weights('param_400_epochs.hdf5')


def predict_font(img):
  im_resized = np.resize(img, (64, 64, 3)).reshape(1, 64, 64, 3).astype("f")
  im_resized /= 255

  pred = model.predict(im_resized)

  return list_row[np.argmax(pred)]
