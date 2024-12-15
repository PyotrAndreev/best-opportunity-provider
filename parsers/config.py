"""
This script is designed for web scraping, interaction with the OpenAI API, and image processing using OCR (Tesseract). 
It includes the following features:

- Web scraping using Selenium and BeautifulSoup.
- Sending requests to the NVIDIA model through the OpenAI API.
- Text recognition using Tesseract OCR.

Modules used in this script:
- requests: for making HTTP requests.
- itertools: utilities for working with iterators.
- bs4 (BeautifulSoup): parsing HTML and XML.
- lxml.etree: working with XML.
- selenium: for controlling a web browser.
- pytesseract: for OCR.
- PIL (Pillow): for image processing.
"""

import requests
import itertools
from bs4 import BeautifulSoup
from lxml import etree 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import urllib, json
from io import BytesIO

from openai import OpenAI

import time
from time import sleep

import pytesseract
from PIL import Image

# Set the path to the Tesseract OCR executable.
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Load a sample JSON file for parsing.
example = open('best-opportunity-provider/parsers/example.json', 'r', encoding='utf-8').read()

# Configure Selenium WebDriver using ChromeDriver.
service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.timeouts = {'pageLoad': 50000}  # Set page load timeout.
# options.add_argument("--headless")  # Option for headless mode.
driver = webdriver.Chrome(service=service, options=options)

# Initialize the OpenAI client for interacting with the NVIDIA API.
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

def question_to_gpt(question: str) -> str:
    """
    Sends a question to the NVIDIA model via the OpenAI API and returns the result.

    Parameters:
    question (str): The question to send to the model.

    Returns:
    str: The response from the model, formatted as a JSON object.

    Example:
    >>> response = question_to_gpt("What is artificial intelligence?")
    >>> print(response)
    { "answer": "Artificial intelligence is ..." }
    """
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "user", "content": question}],
        temperature=0.1,
        top_p=1,
        max_tokens=8192,
        stream=True
    )
    result = ''
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            result += str(chunk.choices[0].delta.content)

    start = -1
    end = -1
    for i in range(len(result)):
        if result[i] == '{' and start == -1:
            start = i
        if result[i] == '}':
            end = i
    return result[start: end + 1]

