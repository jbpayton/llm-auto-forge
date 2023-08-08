import requests
from langchain.tools import tool

@tool("image_downloader", return_direct=False)
def image_downloader(url: str) -> str:
    """This tool downloads an image from a given URL and saves it to a local file."""
    try:
        response = requests.get(url)
        file_path = 'downloaded_image.jpg'
        file = open(file_path, 'wb')
        file.write(response.content)
        file.close()
        return file_path
    except:
        return "Error: " + str(sys.exc_info())