import sys, os
import requests
from langchain.tools import tool

@tool("google_image_search", return_direct=False)
def google_image_search(query: str) -> str:
    """This tool performs a Google Image Search using the Search API and returns a list of image URLs."""
    try:
        API_KEY = os.environ['GOOGLE_API_KEY']
        SEARCH_ENGINE_ID = os.environ['GOOGLE_CSE_ID']
        response = requests.get('https://www.googleapis.com/customsearch/v1', params={'key': API_KEY, 'cx': SEARCH_ENGINE_ID, 'q': query, 'searchType': 'image'})
        response.raise_for_status()
        results = response.json()
        image_urls = [item['link'] for item in results['items']]
        return image_urls
    except:
        return 'Error: ' + str(sys.exc_info())