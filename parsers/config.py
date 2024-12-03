import requests
import itertools
from bs4 import BeautifulSoup
from lxml import etree 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import urllib, json
from PIL import Image
from io import BytesIO
from openai import OpenAI
import time
import pytesseract

# --------------- For getting text from pictures ----------------------
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

example = open('example.json', 'r', encoding='utf-8').read()

# --------------- Create a Browser for getting html code ------------
service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.timeouts = { 'pageLoad': 5000 }
# options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

# --------------- Create a client for GPT ------------------------------
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)