import os
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras import utils as kerasUtils
from PIL import Image
from werkzeug.utils import secure_filename
import numpy as np
import logging
import warnings


warnings.filterwarnings(action="ignore")



logging.basicConfig(filename="log.log", level=logging.WARNING)

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'

class Prediction(object):
    def __init__(self) -> None:
        pass
    
    def loadModel(self):
        try:
            with open('model_labels.pkl', 'rb') as labelPickle:
                modelLabels=pickle.load(labelPickle)[0]
                
            model=load_model('model.keras')
            
            return modelLabels, model
        except Exception as e:
            logging.exception(e)
            
            
    def preprocessImage(self, imageFile):
        try:
            imageArray=kerasUtils.img_to_array(imageFile)
            imageArray=imageArray/255
            imageArray=np.expand_dims(imageArray, axis=0)
            return imageArray
        except Exception as e:
            logging.exception(e)
        
    def makePrediction(self, imagePath):
        try:
            modelLabels, model=self.loadModel()
            
            imageFile=kerasUtils.load_img(path=imagePath, target_size=(224, 224))
            
            imageArray=self.preprocessImage(imageFile=imageFile)
            
            prediction=model.predict(imageArray)
            
            confidence=round(100 * (np.max(prediction[0])), 2)
            
            prediction=modelLabels[np.argmax(prediction[0])]
                    
            return prediction, confidence
        except Exception as e:
            logging.exception(e)
        finally:
            if os.path.exists(imagePath):
                os.remove(imagePath)
                