import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model

img_width, img_height = 150, 150
model_path = './models/yolo.h5'
model_weights_path = './models/yolo_weights.h5'
model = load_model(model_path)
model.load_weights(model_weights_path)

def predict(file):
  x = load_img(file, target_size=(img_width,img_height))
  x = img_to_array(x)
  x = np.expand_dims(x, axis=0)
  array = model.predict(x)
  result = array[0]
  answer = np.argmax(result)
  if answer == 0:
    print("Label: Bike_accident")
  elif answer == 1:
    print("Labels: Car_accident")
  elif answer == 2:
    print("Label: Dog_bite")
  elif answer == 3:
    print("Label: Faint")  

  return answer

predict("d1.jpg")  # Bike Accident
predict("d2.jpg")  # Car Accident 
predict("d3.jpg")  # Dog Bite 
predict("d4.jpg")  # Faint

print("New test")
predict("d5.jpg") # Dog Bite
predict("d6.jpg") # Bike Accident
