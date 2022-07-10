import cv2
from tensorflow.keras.models import load_model as tf_load_model
import base64
import numpy as np

class MLModel:
    """
    A class that helps use an ML model by implementing a few major functions
    """

    def __init__(self, model_path, classes):
        """init function to load model and classes that the model will predict

        Args:
            model_path (str): path where the model file (.h5) exists
            classes (list): list containing the classes the model will predict (order matters)
        """
        self.model = self.load_model(model_path)
        self.classes = classes

    def decode_image(self, str_img):
        """function to decode a base64 encoded image

        Args:
            str_img (str): base64 encoded image string

        Returns:
            np.array: image matrix represented by the string
        """
        data = str_img.split(',')
        encoded_data = data[1] if len(data)>1 else data[0]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img

    def load_model(self, model_path):
        """function to load the model (uses predefined tensorflow function)

        Args:
            model_path (str): path where the model file (.h5) exists

        Returns:
            model: returns tf model
        """
        
        return tf_load_model(model_path)

    def preprocess(self, image, dims, normalize = True):
        """function to preprocess the given image before prediction

        Args:
            image (np.array): image for which a prediction is to be given
            dims (tuple(int)): input size to which the image is to be reshaped
            normalize (bool, optional): if true, image pixels are normalised between 0-1. Defaults to True.

        Returns:
            np.array: preprocessed image
        """
        image = image.astype(np.float32)
        image = cv2.resize(image, dims)
        
        if normalize:
            image /= 255

        return image

    def predict(self, image):
        """function to return prediction for a given image

        Args:
            image (np.array): image for which a prediction is to be given

        Returns:
            str: predicted class name
        """
        image = np.expand_dims(image, axis = 0)
        result = self.model.predict(image)
        return self.classes[np.argmax(result)]