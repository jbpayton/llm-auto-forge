import sys
from PIL import Image
from langchain.tools import tool

@tool("image_displayer", return_direct=False)
def image_displayer(image_path: str) -> str:
    """This tool displays an image from a given local file path."""
    try:
        img = Image.open(image_path)
        img.show()
        return "Image displayed successfully."
    except:
        return "Error: " + str(sys.exc_info())