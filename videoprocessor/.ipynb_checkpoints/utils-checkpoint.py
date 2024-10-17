import cv2
import os
import tensorflow as tf
from django.conf import settings
import shutil
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from keras import backend as K
import numpy as np
from collections import Counter

model=None
def FrameCapture(path):
    output = os.path.join(settings.MEDIA_ROOT, "output")
    ext = "jpg"
    for filename in os.listdir(output):
        file_path = os.path.join(output, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return
    idx = 0
    while cap.isOpened():
        idx += 1
        ret, frame = cap.read()
        if ret:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == 100:
                cv2.imwrite(os.path.join(output, f"frame_0000.{ext}"), frame)
            elif idx < cap.get(cv2.CAP_PROP_FPS):
                continue
            else:
                second = int(cap.get(cv2.CAP_PROP_POS_FRAMES) / idx)
                filled_second = str(second).zfill(4)
                cv2.imwrite(os.path.join(output, f"frame_{filled_second}.{ext}"), frame)
                idx = 0
        else:
            break

# 


def predict(file, num_predictions=10):
    # Clear any existing Keras session to avoid conflicts
    K.clear_session()

    # Load the model within the same graph context
    with tf.Graph().as_default():
        # Load the model
        model_path = os.path.join(settings.MEDIA_ROOT, 'yolo_models', 'yolo_new.h5')
        model_weights_path = os.path.join(settings.MEDIA_ROOT, 'yolo_models', 'yolo_weights_new.h5')
        model = load_model(model_path)
        model.load_weights(model_weights_path)
        
        # Prepare the input image
        img_width, img_height = 150, 150
        x = load_img(file, target_size=(img_width, img_height))
        x = img_to_array(x)
        x = np.expand_dims(x, axis=0)

        # Predict multiple times and store the results
        predictions = []
        for _ in range(num_predictions):
            array = model.predict(x)
            result = array[0]
            answer = np.argmax(result)
            predictions.append(answer)

        # Count the occurrences of each label
        label_counts = Counter(predictions)

        # Find the label with the highest frequency
        most_common_label_index, _ = label_counts.most_common(1)[0]
        labels = ["Bike_accident", "Car_accident", "Dog_bite", "Faint"]
        
        return most_common_label_index, labels[most_common_label_index] if most_common_label_index < len(labels) else None

# def predict(file, num_predictions=10):
#     # Clear any existing Keras session to avoid conflicts
#     K.clear_session()

#     # Load the model within the same graph context
#     with tf.Graph().as_default():
#         # Load the model
#         model_path = os.path.join(settings.MEDIA_ROOT, 'yolo_models', 'yolo_new.h5')
#         model_weights_path = os.path.join(settings.MEDIA_ROOT, 'yolo_models', 'yolo_weights_new.h5')
#         model = load_model(model_path)
#         model.load_weights(model_weights_path)
        
#         # Prepare the input image
#         img_width, img_height = 150, 150
#         x = load_img(file, target_size=(img_width, img_height))
#         x = img_to_array(x)
#         x = np.expand_dims(x, axis=0)

#         # Predict multiple times and store the results
#         predictions = []
#         for _ in range(num_predictions):
#             array = model.predict(x)
#             result = array[0]
#             answer = np.argmax(result)
#             predictions.append(answer)

#         # Count the occurrences of each label
#         label_counts = Counter(predictions)

#         # Find the label with the highest frequency
#         most_common_label_index, _ = label_counts.most_common(1)[0]
#         labels = ["Bike_accident", "Car_accident", "Dog_bite", "Faint"]
#         label_text = labels[most_common_label_index] if most_common_label_index < len(labels) else "Unknown"

#         # Return the result in the desired format
#         return f"The result is {label_text}"


def start_predictions():
    lst = []
    output = os.path.join(settings.MEDIA_ROOT, "output")
    for root, _, files in os.walk(output):
        for filename in files:
            if filename.startswith("."):
                continue
            file_path = os.path.join(root, filename)
            _, result = predict(file_path)
            if result:
                lst.append(result)
    print(lst)
    return lst
