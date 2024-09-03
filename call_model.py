import requests
import json
import base64
from io import BytesIO
from PIL import Image
import os

URL = 'https://m-2cdaff0852124e0c8659af40827a4996-m.default.model-v1.inferless.com/v2/models/Animagine-xl-3.1_2cdaff0852124e0c8659af40827a4996/versions/1/infer'
headers = {"Content-Type": "application/json", "Authorization": "Bearer e0cee946ceedd0c7fbadee19f66c818de29fc42180cd2664ea0da5dae57cb088666df25ba07cf2e309639d342320fcb15d7ec8d14c38ff8d33cdcc1049197eea"}

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

    static_folder = 'static'
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
    
    image_filename = f"generated_image_{hash(prompt)}.png"
    image_path = os.path.join(static_folder, image_filename)
    
    image.save(image_path)
    
    return image_path