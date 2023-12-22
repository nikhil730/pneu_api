import os
os.environ["KERAS_BACKEND"] = "tensorflow"
import tensorflow as tf
import keras
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from keras.preprocessing import image
from fastapi import FastAPI
from tensorflow import expand_dims
from numpy import argmax
from numpy import max
import numpy as np
from json import dumps
from PIL import Image
from uvicorn import run
# from tensorflow.keras.models import load_model
# from tensorflow.keras.utils import get_file 
# from tensorflow.keras.utils import load_img 
# from tensorflow.keras.utils import img_to_array


import numpy as np
model_dir="model/"
MODEL = tf.saved_model.load(model_dir)
prediction_function = MODEL.signatures['serving_default']

# model = keras.models.Sequential([MODEL])

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def index():
    return {"Message": "This is Index"}
# uvicorn main:app --reload
@app.post('/predict/')
async def predict(file: UploadFile=File(...)):
    image = Image.open(file.file)
    # img_path = keras.utils.get_file(
    #     origin = image_link
    # )
    # img_width, img_height = 299, 299
    # img = image.keras.utils.load_img(img_path, target_size = (img_width, img_height))
    img = keras.utils.img_to_array(image)/255
    img.resize((150,150,1))
    img = np.expand_dims(img, axis = 0)
    #print(img)
    # img=tf.convert_to_tensor(img)
    input_data=tf.constant(img, dtype=tf.float32)
    # predictions = prediction_function(x=input_data)
    prediction=MODEL(img)
    predictions=prediction_function(conv2d_input=input_data)
    # print(predictions)
    print(predictions)
    print(prediction.numpy()[0][0])
    if(prediction.numpy()[0][0]>0.5):
        return "positive"
    
    else:
        return "Negative"