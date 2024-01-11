import requests
import os
import json
import base64
from dotenv import load_dotenv

load_dotenv()

def get_headers():
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {os.getenv('STABLE_DIFUSION_KEY')}"
    }
    return headers

def get_image(prompt: str):
    url = "https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image"

    payload = {
        "model": "stable-diffusion-xl-v1-0",
        "prompt": f"{prompt}",
        "negative_prompt": "Disfigured, cartoon, blurry",
        "width": 512,
        "height": 512,
        "steps": 30,
        "guidance": 7.5,
        "seed": 0,
        "scheduler": "euler",
        "output_format": "png"
    }
    
    headers = get_headers()
    response = requests.post(url, json=payload, headers=headers)
    response_dict = response.json()
    image_bytes = base64.b64decode(response_dict['image'])
    return image_bytes