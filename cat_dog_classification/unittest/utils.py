import requests
import base64
import json

from enum import Enum

class TargetURL(Enum):
    LOCALHOST = 'http://localhost:7998/cat-dog_classification'

#Metodo que conver
def make_request(target_url, image):
    encoded_img = None
    with open(image, "rb") as image_file_f:
        buffer_front = image_file_f.read()
        encoded_img = base64.b64encode(buffer_front).decode("utf-8")

    headers = {'Content-Type': 'application/json'}

    json_dict = {'image_b64': encoded_img}
    response = requests.post(target_url.value, headers=headers, json=json_dict)
    
    return response


