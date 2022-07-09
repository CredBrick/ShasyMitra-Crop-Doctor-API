import cv2
import os
from . import exceptions
from tensorflow.keras.models import load_model as tf_load_model
import tensorflow as tf
import base64
import numpy as np

class MLModel:
    """
    A class that helps use an ML model by implementing a few major functions
    """

    def __init__(self, model_path, classes):
        self.model = self.load_model(model_path)
        self.classes = classes

    def decode_image(self, str_img):
        encoded_data = str_img.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img

    def load_model(self, model_path):
        
        return tf_load_model(model_path)

    def preprocess(self, image, dims, normalize = True):
        """
        Preprocessing function for the given model
        Args:
            image (string/numpy.ndarray): A numpy array image or a filepath

        Returns:
            processed_image: The processed image that can directly be fed into the model
        """

        image = image.astype(np.float32)
        image = cv2.resize(image, dims)
        
        if normalize:
            image /= 255

        return image

    def predict(self, image):
        image = np.expand_dims(image, axis = 0)
        result = self.model.predict(image)
        return self.classes[np.argmax(result)]