import json
from typing import Type

import requests
from bs4 import BeautifulSoup
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import BaseTool
from langchain.vectorstores import Chroma
from pydantic import BaseModel, Field


class ToolRegistry:
    _instance = None
    _embeddings = None
    _vector_store = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._embeddings = None
        self._vector_store = None

    def add_documents(self, docs):
        if self._embeddings is None:
            self._embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        if self._vector_store is None:
            self._vector_store = Chroma.from_documents(docs, self._embeddings)
        else:
            self._vector_store.add_documents(docs)

    def query_website(self, url: str, query: str):
        self.scrape_website(url)
        filter_dict = dict()
        filter_dict["url"] = url
        results = self._vector_store.similarity_search_with_score(query, 5, filter=filter_dict)
        print(results[0])

    def scrape_website(self, url: str):
        print("Scraping website...")

        # Make the request
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text()
            links = [a['href'] for a in soup.find_all('a', href=True)]

            text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=1000, chunk_overlap=200)
            docs = text_splitter.create_documents([text], metadatas=[{"url": url, "type": "text"}])
            self.add_documents(docs)

        else:
            print(f"HTTP request failed with status code {response.status_code}")



class ScrapeWebsiteInput(BaseModel):
    """Inputs for scrape_website"""
    objective: str = Field(
        description="The objective & task that users give to the agent")
    url: str = Field(description="The url of the website to be scraped")


class ScrapeWebsiteTool(BaseTool):
    name = "scrape_website"
    description = "useful when you need to get data from a website url, passing both url and objective to the function; DO NOT make up any url, the url should only be from the search results"
    args_schema: Type[BaseModel] = ScrapeWebsiteInput

    def _run(self, objective: str, url: str):
        return NotImplementedError("error here")

    def _arun(self, url: str):
        raise NotImplementedError("error here")


if __name__ == "__main__":
    ToolRegistry().query_website('https://blazblue.fandom.com/wiki/Rachel_Alucard',
                                 'What does Rachel Alucard think about bell peppers?')