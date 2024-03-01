from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import pandas as pd


class QuoteScraper:
    def __init__(self, path):
        self._DRIVER_PATH = path
        self._authors_details = {
                    "Name"             : [],
                    "Nationality"      : [],
                    "Description"      : [],
                    "Date of Birth"    : [], 
                  }

        # convert driver page source to soup object
    @staticmethod
    def driver_to_soup(driver_source_page):
        return BeautifulSoup(driver_source_page, "html.parser")
    
    def _save_to_csv(self, file_name) -> None:
        data_frame = pd.DataFrame(self._authors_details)
        data_frame.to_csv(f"{file_name}.csv", index=False)
        print(f"{file_name}.csv was saved successfully")
        return None
        
        
    def _initialize_driver(self):
        chrome_service = webdriver.ChromeService(executable_path=self._DRIVER_PATH)
        # options = webdriver.ChromeOptions()
        return webdriver.Chrome(service=chrome_service)
    
    # Method to format the location
    @staticmethod
    def _format_location(location_list):
        try:
            in_index = int(location_list.index("in"))
        except: 
            return None
        return " ".join(location_list[in_index+1:])
    
    # Methods to get the required quotes
    def scrape_quotes(self):
        driver = self._initialize_driver()
        page_count = 1
        while len(self._authors_details["Name"]) < 20:
            url = f"https://quotes.toscrape.com/page/{page_count}/"
            driver.get(url)
            
            # Waits for 10 secs 
            driver.implicitly_wait(10)
            # Converting to soup
            soup = self.driver_to_soup(driver.page_source)
            
            authors = soup.find_all("div", class_="quote")
            for author in authors:
                author_link = author.find("a", href=True)["href"]
                # Get the content of author's details
                driver.get(f"https://quotes.toscrape.com{author_link}")
                
                # Waits for 5 secs 
                driver.implicitly_wait(5)
                # Converting to soup
                soup = self.driver_to_soup(driver.page_source)
                
                # Populating the authors_details dict
                self._authors_details["Name"].append( soup.find("h3", class_="author-title").text.strip() )
                location_text_list = soup.find("span", class_="author-born-location").text.strip().split(" ")
                self._authors_details["Nationality"].append( self._format_location(location_text_list) )
                self._authors_details["Description"].append( soup.find("div", class_="author-description").text.strip() )
                self._authors_details["Date of Birth"].append( soup.find("span", "author-born-date").text.strip() )
                
        # Saving the authors quotes to csv files
        self._save_to_csv("AuthorsQuotes")
        driver.quit()


# Implementation
DRIVER_PATH = "chromedriver_win32/chromedriver.exe"
scraper = QuoteScraper(DRIVER_PATH)
scraper.scrape_quotes()







# authors_set = set()
# authors_list = []

# # Extract authors from the first page
# for author in soup.select('.author'):
#     if len(authors_set) >= 10:
#         break
#     author_url = url + author.parent['href']
#     if author.text not in authors_set:
#         authors_set.add(author.text)
#         authors_list.append({'name': author.text, 'url': author_url})

# # Extract additional authors from subsequent pages until we have 20
# page = 1
# while len(authors_set) < 20:
#     page += 1
#     next_url = f'{url}page/{page}/'
#     response = requests.get(next_url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     for author in soup.select('.author'):
#         if len(authors_set) >= 20:
#             break
#         author_url = url + author.parent['href']
#         if author.text not in authors_set:
#             authors_set.add(author.text)
#             authors_list.append({'name': author.text, 'url': author_url})

# # Now scrape detailed information for each author
# authors_data = []
# for author_info in authors_list:
#     response = requests.get(author_info['url'])
#     soup = BeautifulSoup(response.text, 'html.parser')
#     author_details = soup.find('div', class_='author-details')
#     nationality = author_details.find('span', class_='author-born-country').text.strip()
#     description = author_details.find('div', class_='author-description').text.strip()
#     date_of_birth = author_details.find('span', class_='author-born-date').text.strip()
#     authors_data.append({'name': author_info['name'], 'nationality': nationality, 'description': description, 'date_of_birth': date_of_birth})

# # Print the scraped data
# for author in authors_data:
#     print(author)