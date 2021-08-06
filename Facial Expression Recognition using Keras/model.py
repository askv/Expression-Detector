from tensorflow.keras.models import model_from_json
import numpy as np
import tensorflow as tf


#to cope up with this error(failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED)
config = tf.compat.v1.ConfigProto(gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)
# device_count = {'GPU': 1}
)
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(session)



class FacialExpressionModel(object):

	emotions_list = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'sad', 'surprise']

	def __init__(self, model_json_file, model_weights_file):
		with open(model_json_file,'r') as json_file:
			loaded_model_json = json_file.read()
			self.loaded_model = model_from_json(loaded_model_json)

		self.loaded_model.load_weights(model_weights_file)
		self.loaded_model._make_predict_function()

	def predict_emotion(self,img):	
		self.preds = self.loaded_model.predict(img)
		return FacialExpressionModel.emotions_list[np.argmax(self.preds)] 