import sys

from PIL import Image, ImageDraw
from transformers import pipeline

from langchain.tools import tool

@tool("image_recognition_and_captioning", return_direct=False)
def image_recognition_and_captioning(image_path: str, output_path: str) -> str:
    """This tool recognizes the content of an image and adds a caption to it."""

    try:
        # Create a pipeline for image recognition
        image_recognition = pipeline('image-classification')

        # Open the image file
        img = Image.open(image_path)

        # Perform image recognition
        result = image_recognition(img)

        # Get the label of the image
        label = result[0]['label']

        # Create a draw object
        draw = ImageDraw.Draw(img)

        # Add the caption to the image
        draw.text((10, 10), label, fill='white')

        # Save the captioned image
        img.save(output_path)

        return 'Finished running tool.'
    except:
        # If there is an error, print the error to the console.
        return 'Error: ' + str(sys.exc_info())