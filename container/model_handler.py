import os
import json
import sys
import logging
import pickle
import time
import gzip
import catboost
from catboost import CatBoostClassifier, Pool as CatboostPool, cv
import pandas as pd
import io   

#JSON_CONTENT_TYPE = 'application/json'
#PRE_TRAINED_MODEL_NAME = 'roberta-base'
#CLASS_NAMES = ['negative', 'neutral', 'positive']

logger = logging.getLogger(__name__)

import os

class ModelHandler(object):
    
    def __init__(self):
        start = time.time()
        self.initialized = False
        print(f" perf __init__ {(time.time() - start) * 1000} ms")

    def initialize(self, ctx):
        start = time.time()
        self.device = 'cpu'
        
        properties = ctx.system_properties
        self.device = 'cpu'
        model_dir = properties.get('model_dir')
        
        print('model_dir {}'.format(model_dir))
        print(os.system("ls {}".format(model_dir)))

        model_file = CatBoostClassifier()
        self.model = model_file = model_file.load_model("{}/catboost_model.bin".format(model_dir))
        self.initialized = True
        print(f" perf initialize {(time.time() - start) * 1000} ms")

    def preprocess(self, input_data):
        """
        """
        
        start = time.time()
        print(type(input_data))
        output= input_data
        print(f" perf preprocess self.model {(time.time() - start) * 1000} ms")
        return output

    def inference(self, inputs):
        """
        """
        start = time.time()
        #print(inputs)
        predictions = self.model.predict_proba(inputs)
        print(f" perf inference {(time.time() - start) * 1000} ms")
        return predictions
        #return inputs

    def postprocess(self, inference_output):
        start = time.time()
        inference_output = dict(enumerate(inference_output.flatten(), 1))
        print(f" postprocess {(time.time() - start) * 1000} ms")
        return [inference_output]
    
    def handle(self, data, context):
        """
        Invoke by TorchServe for prediction request.
        Do pre-processing of data, prediction using model and postprocessing of prediciton output
        :param data: Input data for prediction
        :param context: Initial context contains model server system properties.
        :return: prediction output
        """
        start = time.time()
        
        print(type(data))
        
        input_data = data[0]['body'].decode()
        print(type(input_data))
        df = pd.read_csv(io.StringIO(input_data))
        print(df)
       
        model_input = self.preprocess(df)
        model_output = self.inference(model_input)
        print(f" perf handle_in {(time.time() - start) * 1000} ms")
        return self.postprocess(model_output)
    
    
_service = ModelHandler()

def handle(data, context):
    start = time.time()
    if not _service.initialized:
        _service.initialize(context)

    if data is None:
        return None
    
    print(f" perf handle_out {(time.time() - start) * 1000} ms")
    return _service.handle(data, context)
    