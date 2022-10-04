YOUR_TOKEN="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"
PYTORCH_CUDA_ALLOC_CONF="garbage_collection_threshold:0.6,max_split_size_mb:128"

from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=YOUR_TOKEN) #type:ignore

pipe.to("cuda")

#download and test
pipe("Pink football", guidance_scale=7.5, num_inference_steps=1, height=1, width=1)

