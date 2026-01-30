# import time
# from google import genai
# from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

# client = genai.Client(api_key=API_KEY)

# prompt = """A super cat is the boss of all the gangs. The tiger was attacked by cat gangs but the boss saved the tiger by fighting with group of cats. 
# '"""

# operation = client.models.generate_videos(
#     model="veo-3.1-generate-preview",
#     prompt=prompt,
# )

# # Poll the operation status until the video is ready.
# while not operation.done:
#     print("Waiting for video generation to complete...")
#     time.sleep(10)
#     operation = client.operations.get(operation)

# # Download the generated video.
# generated_video = operation.response.generated_videos[0]
# client.files.download(file=generated_video.video)
# generated_video.video.save("dialogue_example.mp4")
# print("Generated video saved to dialogue_example.mp4")

from google import genai
from google.genai import types

client = genai.Client(api_key=API_KEY)

# Load your image and set up your prompt
with open(r'app\img_objects.avif', 'rb') as f:
    image_bytes = f.read()

prompt = """
      Return bounding boxes as a JSON array with labels. Never return masks
      or code fencing. Limit to 25 objects. Include as many objects as you
      can identify on the table.
      If an object is present multiple times, name them according to their
      unique characteristic (colors, size, position, unique characteristics, etc..).
      The format should be as follows: [{"box_2d": [ymin, xmin, ymax, xmax],
      "label": <label for the object>}] normalized to 0-1000. The values in
      box_2d must only be integers
      """

image_response = client.models.generate_content(
  model="gemini-robotics-er-1.5-preview",
  contents=[
    types.Part.from_bytes(
      data=image_bytes,
      mime_type='image/jpeg',
    ),
    prompt
  ],
  config = types.GenerateContentConfig(
      temperature=0.5,
      thinking_config=types.ThinkingConfig(thinking_budget=0)
  )
)

print(image_response.text)