#Importando bibliotecas
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from enum import Enum
from model_runner import *
from utils import *

# Definindo classes e Enums uteis.
class SuccessResponse(BaseModel):
    status: str
    pet_type: str
    model_conf: float

class PredictionError(BaseModel):
    status: str
    msg: str

class Classification_Request(BaseModel):
    image_b64: str

class FEEDBACK_MSG(Enum):
    INVALID_B64 = 'Image base64 invalid'    

class STATUS(Enum):
    SUCCESS = 'Success'
    FAILED = 'Failed'

#Criando um ModelRunner.
M_RUNNER = ModelRunner()

#Criação da API.
app = FastAPI(title='Deploying Cat-Dog Classification Service with FastAPI')

#Definição do endpoint.
@app.post("/cat-dog_classification") 
async def cat_dog_classification(req: Classification_Request):
    
    #Preparando imagens para B64.
    img_b64 = req.image_b64
    isbase64f = isBase64(img_b64)
    if (not isbase64f):
        err_output = PredictionError(status = STATUS.FAILED.value, msg = FEEDBACK_MSG.INVALID_B64.value)
        return err_output

    #Realizando classificação.
    label, conf = M_RUNNER.predict_animal(img_b64)
    response = SuccessResponse(status = STATUS.SUCCESS.value, pet_type = label, model_conf = conf)
    return response

#Executando a API.            
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7998, log_level="info")   

