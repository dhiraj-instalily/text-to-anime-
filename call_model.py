import requests
import json
import base64
from io import BytesIO
from PIL import Image
import os
from config import URL, API_KEY, STATIC_FOLDER

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

def generate_image(prompt, negative_prompt):
    data = {
        "inputs": [
            {
                "name": "prompt",
                "shape": [1],
                "data": [prompt],
                "datatype": "BYTES"
            },
            {
                "name": "negative_prompt",
                "shape": [1],
                "data": [negative_prompt],
                "datatype": "BYTES"
            }
        ]
    }

    response = requests.post(URL, headers=headers, data=json.dumps(data))
    response_data = response.json()

    base64_image = response_data['outputs'][0]['data'][0]
    image_data = base64.b64decode(base64_image)
    image_buffer = BytesIO(image_data)
    image = Image.open(image_buffer)

    if not os.path.exists(STATIC_FOLDER):
        os.makedirs(STATIC_FOLDER)
    
    image_filename = f"generated_image_{hash(prompt)}.png"
    image_path = os.path.join(STATIC_FOLDER, image_filename)
    
    image.save(image_path)
    
    return image_path