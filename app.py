import os

#set your own diffusers token here (as an env var)
YOUR_TOKEN=os.environ.get('YOUR_TOKEN')

PYTORCH_CUDA_ALLOC_CONF="garbage_collection_threshold:0.6,max_split_size_mb:128"

from flask import Flask
from datetime import datetime
from flask import send_file
import io
import re
import torch
from PIL import Image as PILImage
from diffusers import StableDiffusionPipeline

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

@app.route('/create_image/<prompt>')
def get_image(prompt):

    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=YOUR_TOKEN) #type:ignore

    pipe.to("cuda")
    #pipe.safety_checker = lambda images, a: images, False

    image = pipe(prompt, guidance_scale=7.5, num_inference_steps=50, height=512, width=512)["sample"]

    Bio = io.BytesIO()
    image[0].save(Bio, 'JPEG')
    Bio.seek(0)

    return send_file(Bio, mimetype='image/jpeg')