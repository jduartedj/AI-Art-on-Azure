import os

#set your own diffusers token here (as an env var)
YOUR_TOKEN=os.environ.get('YOUR_TOKEN')

from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=YOUR_TOKEN) #type:ignore

#download and test
pipe("Pink football", guidance_scale=7.5, num_inference_steps=1, height=64, width=64)

