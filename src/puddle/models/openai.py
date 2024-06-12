from openai import OpenAI
import requests
from PIL import Image
import base64
from io import BytesIO
import os

import puddle.prompts as pp

def configure_ask(model = "gpt-3.5-turbo"):
    """
    Make a function that will answer text questions with text answers.
    """

    client = OpenAI()

    def ask(system_prompt : str, user_prompt : str = pp.default_system_prompt) -> str:

        completion = client.chat.completions.create(
          model=model,
          messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
          ]
        )

        response = completion.choices[0].message.content

        if response is not None:
            return response
        else:
            raise ValueError("No response")

    return ask

def configure_dalle():

    client = OpenAI()

    def dalle(
        prompt,
        model = "dall-e-3",
        size = "1024x1024",
        quality = "standard",
        user="George Washington",
        basename = "dalle"
    ):

        params = {
          "model" : model,
          "prompt" : prompt,
          "size" : size,
          "quality" : quality, # options: standard, hq
          "n" : 1,
          "user" : user,
          "response_format": "b64_json",
          "style" : "natural" # options: natural, vivid, ...
        }

        response = client.images.generate(**params)

        # dalle-e-3 rewrites the prompt
        revised_prompt = response.data[0].revised_prompt
        print(f"Revised prompt: {revised_prompt}")

        images_data = [image.model_dump()["b64_json"] for image in response.data]

        # Dump data to png
        i = 1
        for data in images_data:
            image = Image.open(BytesIO(base64.b64decode(data)))
            while os.path.exists(f"{basename}_{i}.png"):
                  i += 1
            i += 1
            image.save(f"{basename}_{i}.png")

    return dalle
