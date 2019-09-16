from __future__ import print_function
import requests
import json
import cv2
from PIL import Image
import os

addr = 'http://localhost:5000'
test_url = addr + '/flowimg'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('imageis.jpg')
print(img)
 
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
print(response.text)

# # expected output: {u'message': u'image received. size=124x124'}

# image =  Image.open(os.getcwd()+'/imageis.jpg')
# img = open(image, 'rb').read()
# response = requests.post(test_url, data=img, headers=headers)
 
#{"py/set": ["\n1/1 [==============================] - 1s 957ms/step\n[\n  {\n    \"image_id\": \"testimage\",\n    \"mean_score_prediction\": 4.923994995653629\n  }\n]\n"]}
