import sys
from PIL import Image, ImageDraw, ImageFont
from langchain.tools import tool

@tool("meme_creator", return_direct=False)
def meme_creator(image_path: str, top_text: str, bottom_text: str) -> str:
    """This tool creates a meme with the given image and text."""
    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('arial.ttf', size=45)
        draw.text((10, 10), top_text, fill='white', font=font)
        draw.text((10, image.height - 60), bottom_text, fill='white', font=font)
        image.save('meme.png')
        return 'Meme created successfully.'
    except:
        return 'Error: ' + str(sys.exc_info())