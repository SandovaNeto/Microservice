import cv2
import base64
import numpy as np
import re

#Verifica se a imagem em base64 é valida.
def isBase64(s):
    RegEx_result = re.search("[0-9]+([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?", s)
    if RegEx_result is not None:
        return True
    else:
        return False

#Converte uma imagem para base64.
def image_to_b64(image):
    enconde_params= [cv2.IMWRITE_JPEG_QUALITY, 95]
    ret, buf = cv2.imencode('.jpg', image, enconde_params)
    img_return = buf.tobytes()
    encoded_img_face = base64.b64encode(img_return)
    return encoded_img_face      

#Converte um base64 para imagem.
def DecodeImgFromB64(image_base64):
    decoded = base64.b64decode(image_base64)
    nparr = np.frombuffer(decoded, np.uint8)
    bgr_img = cv2.imdecode(nparr, flags=cv2.IMREAD_COLOR)
    rgb_img = bgr_img[...,::-1].copy()
    return rgb_img
