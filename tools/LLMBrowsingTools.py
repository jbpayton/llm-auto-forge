import re

import requests
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import tool
from langchain.vectorstores import Chroma
import markdownify


class WebScrapingCache:
    _instance = None
    _initialised = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebScrapingCache, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if WebScrapingCache._initialised:
            return
        WebScrapingCache._initialised = True
        self._embeddings = None
        self._vector_store = None
        self._url_list = []

    def add_documents(self, docs):
        if self._embeddings is None:
            self._embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        if self._vector_store is None:
            self._vector_store = Chroma.from_documents(docs, self._embeddings)
        else:
            self._vector_store.add_documents(docs)

    def query_website(self, url: str, query: str, keep_links: bool = False):
        self.scrape_website(url, keep_links=keep_links)
        filter_dict = dict()
        filter_dict["url"] = url
        results = self._vector_store.max_marginal_relevance_search(query, 3, filter=filter_dict)
        return results

    def paged_read(self, url: str, page: int, keep_links: bool = False):
        docs = self.scrape_website(url, keep_links=keep_links, chunk_size=2000, chunk_overlap=0, cache=False)
        if docs is None:
            return "Error scraping website"
        if page > len(docs):
            return "Page not found"
        return str(docs[page]) + "\n\n" + f" = Page {page} of {len(docs)-1}"

    def scrape_website(self, url: str, keep_links=False, chunk_size=1024, chunk_overlap=128, cache=True):
        link_suffix = "(Keep links)" if keep_links else ""
        if url + link_suffix in self._url_list and cache:
            print("Site in cache, skipping...")
            return

        print("Scraping website...")

        # Make the request
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            if keep_links:
                tags_to_strip = []
            else:
                tags_to_strip = ['a']

            # Remove script and style tags (and meta tags)
            stripped_text = re.sub(r'<script.*?</script>', '', str(response.content))
            stripped_text = re.sub(r'<style.*?</style>', '', str(stripped_text))
            stripped_text = re.sub(r'<meta.*?</meta>', '', str(stripped_text))

            text = markdownify.markdownify(stripped_text, strip=tags_to_strip)

            # Removing \n and \t
            text = re.sub(r'\\n|\\t', '', text)

            # Removing emoji sequences (unicode escape sequences)
            text = re.sub(r'\\x[0-9a-f]{2}', '', text)

            # split the text into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                           chunk_overlap=chunk_overlap)
            docs = text_splitter.create_documents([text], metadatas=[{"url": url}])
            if cache:
                self.add_documents(docs)
                self._url_list.append(url + link_suffix)

            return docs

        else:
            print(f"HTTP request failed with status code {response.status_code}")
            return f"HTTP request failed with status code {response.status_code}"


@tool("query_website", return_direct=False)
def query_website(website_url: str, query: str, keep_links: bool = False) -> str:
    """useful when you need to get data from a website url, passing both url and the query to the function; DO NOT
    make up any url, the url should only be from the search results. Links can be enabled or disabled as needed. """
    return str(WebScrapingCache().query_website(website_url, query, keep_links=keep_links))


@tool("paged_web_browser", return_direct=False)
def paged_web_browser(website_url: str, page: int) -> str:
    """useful when you need to read data from a website without overflowing context, passing both url and the page number (zero indexed) to the function; DO NOT
    make up any url, the url should only be from the search results. Links can be enabled or disabled as needed. """
    return str(WebScrapingCache().paged_read( website_url, page))


if __name__ == "__main__":
    query = "What does Rachel Alucard look like?"
    print(query)
    results = WebScrapingCache().query_website('https://blazblue.fandom.com/wiki/Rachel_Alucard', query)
    print(str(results))

    query = "Rachel Alucard and bell peppers?"
    print(query)
    results = WebScrapingCache().query_website('https://blazblue.fandom.com/wiki/Rachel_Alucard', query)
    print(str(results))

    doc = WebScrapingCache().paged_read('https://www.deeplearning.ai/resources/natural-language-processing/', 5)
    print(doc)
