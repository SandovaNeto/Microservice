import os
import yaml
import pprint
import base64
import numpy as np
from io import BytesIO
from PIL import Image, ImageOps

from fastapi import FastAPI
from pydantic import BaseModel

import tensorflow as tf
import grpc
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc


class ModelRunner: #Definição da classe Model Runner.
    def __init__(self): #Definição do Init.
        self.experiment_id  = None
        self.model_input_name = None
        self.model_output_name = None
        self.__set_configs()
        self.stub = None
        self.__create_service_stub()
          
    def __set_configs(self): #Metodo set das configurações do modelo.
        configs = None
        with open('config.yaml') as file:
            configs = yaml.load(file, Loader=yaml.FullLoader)
            print('config.yaml file:')
            pprint.pprint(configs)
        self.experiment_id  = configs['experiment_id']
        self.model_input_name = configs['model_input_name']
        self.model_output_name = configs['model_output_name']
    
    def __create_service_stub(self): #Criação do Stub do GRPC para comunicação com iimagem do tensorflow serving.
        host = os.getenv('SERVICE_MODEL_HOST')
        port = os.getenv('SERVICE_MODEL_PORT')
        print("TRYING TO CONNECT TO PORT: ", port)
        GRPC_MAX_RECEIVE_MESSAGE_LENGTH = 4096 * 4096 * 3
        channel = grpc.insecure_channel(f'{host}:{port}', options=[('grpc.max_receive_message_length', GRPC_MAX_RECEIVE_MESSAGE_LENGTH)])
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    def __create_grpc_request(self, image, model_name, signature_name='serving_default'): #Criação do GRPC request do tensorflow serving.
        grpc_request = predict_pb2.PredictRequest()
        grpc_request.model_spec.name = model_name
        grpc_request.model_spec.signature_name = signature_name
        grpc_request.inputs[self.model_input_name].CopyFrom(tf.make_tensor_proto(image, shape=image.shape))
        return grpc_request

    def preprocess_classifier_image(self, im_b64): #Preprocessamento da imagem
        im_bytes = base64.b64decode(im_b64)
        im_file = BytesIO(im_bytes)
        image = Image.open(im_file).convert('RGB')
        np.set_printoptions(suppress=True)
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        return data
  
    def predict_animal(self, image): #Fluxo completo de predição e retorno de resultado.
        
        data = self.preprocess_classifier_image(image)

        grpc_request = self.__create_grpc_request(data, self.experiment_id)
        result = self.stub.Predict(grpc_request, 10)

        result_idx_0 = result.outputs[self.model_output_name].float_val[0] #cat
        result_idx_1 = result.outputs[self.model_output_name].float_val[1] #dog
        all_results = [result_idx_0, result_idx_1]
        print("RESULT: ",all_results)

        label_indexes = {0:'CAT', 1: 'DOG'}
        y_hat = np.argmax(all_results)
        pred_label = label_indexes[y_hat]
        conf = round(np.max([result_idx_0, result_idx_1])*100, 2)

        return pred_label, conf

 