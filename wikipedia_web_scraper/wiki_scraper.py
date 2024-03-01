import requests
from bs4 import BeautifulSoup
import random

# Get a random Wikipedia page
random_page_url = 'https://en.wikipedia.org/wiki/Special:Random'
response = requests.get(random_page_url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the title and content of the random page
title = soup.find('h1', class_='firstHeading').text
content_paragraphs = soup.find_all('p')

# Print the title and the first few paragraphs of the content
print(f'Title: {title}\n')
print('Content:')
for paragraph in content_paragraphs[:3]:
    print(paragraph.text)
