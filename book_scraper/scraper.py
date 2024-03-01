from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import pandas as pd
import time


class Scraper:
    def __init__(self, path, pages_to_scrape):
        self._pages_to_scrape = pages_to_scrape
        self._DRIVER_PATH = path
        self._df = {
                    "Book Name"             : [],
                    "Price"                 : [],
                    "Stock Status"          : [],
                    "Rating"                : [],
                    "Description"           : [],
                    "Category"              : [],
                    "UPC"                   : [],
                    "Product Type"          : [],
                    "Price (excl. tax)"     : [],
                    "Price (incl. tax)"     : [],
                    "Tax"                   : [],
                    "Availability"          : [],
                    "Number of reviews"     : [],    
                  }
    
    # convert driver page source to soup object
    @staticmethod
    def driver_to_soup(driver_source_page):
        return BeautifulSoup(driver_source_page, "html.parser")
    
    def _save_to_csv(self, file_name) -> None:
        data_frame = pd.DataFrame(self._df)
        data_frame.to_csv(f"{file_name}.csv", index=False)
        print(f"{file_name}.csv was saved successfully")
        return None
        
        
    def _initialize_driver(self):
        chrome_service = webdriver.ChromeService(executable_path=self._DRIVER_PATH)
        # options = webdriver.ChromeOptions()
        return webdriver.Chrome(service=chrome_service)
    

    def scrape(self):
        driver = self._initialize_driver()
        for page_number in range(1, self._pages_to_scrape+1):
            url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
            driver.get(url)
            
            # Waits for 10 secs 
            driver.implicitly_wait(10)
            
            # Converting to soup
            soup = self.driver_to_soup(driver.page_source)
            # Scrapping the books
            books = soup.find_all('article', class_='product_pod')
            
            # Getting the required fields from the books
            for book in books:
                self._df["Book Name"].append( book.h3.a['title'].strip() )
                self._df["Price"].append( book.find('p', class_='price_color').text.strip() )       
                self._df["Rating"].append( book.p['class'][1].strip() )  
                
                # # Visiting the books details
                book_link = book.h3.a["href"]
                book_details_link = f"https://books.toscrape.com/catalogue/{book_link}"
                driver.get(book_details_link)
                
                 # Waits for 5 secs 
                driver.implicitly_wait(5)
                
                 # Converting to soup
                soup = self.driver_to_soup(driver.page_source)
                
                # Scraping more of the book
                self._df["Stock Status"].append( soup.find("th", string="Availability").find_next("td").text.strip() )
                self._df["Description"].append( soup.find("meta", attrs={"name": "description"})["content"].strip() )
                self._df["UPC"].append( soup.find("th", string="UPC").find_next("td").text.strip() )
                self._df["Category"].append( soup.find("a", href=True, string="Books").find_next("a").text.strip() )
                self._df["Product Type"].append( soup.find("th", string="Product Type").find_next("td").text.strip() )     
                self._df["Price (excl. tax)"].append( soup.find("th", string="Price (excl. tax)").find_next("td").text.strip() )
                self._df["Price (incl. tax)"].append( soup.find("th", string="Price (incl. tax)").find_next("td").text.strip() )
                self._df["Tax"].append( soup.find("th", string="Tax").find_next("td").text.strip() )              
                self._df["Availability"].append( soup.find("th", string="Availability").find_next("td").text.strip() )   
                self._df["Number of reviews"].append( soup.find("th", string="Number of reviews").find_next("td").text.strip() )
                
        # print("--------------------------------------")
        # print(f'Total Book name {len(self._df["Book Name"])}')
        # print(f'Total price {len(self._df["Price"])}')
        # print(f'Total Rating {len(self._df["Rating"])}')
        # print(f'Total stock status {len(self._df["Stock Status"])}')
        # print(f'Total Description {len(self._df["Description"])}')
        # print(f'Total UPC {len(self._df["UPC"])}')
        # print(f'Total Category {len(self._df["Category"])}')
        # print(f'Total Product Type {len(self._df["Product Type"])}')
        # print(f'Total Price (excl. tax) {len(self._df["Price (excl. tax)"])}')
        # print(f'Total Price (incl. tax) {len(self._df["Price (incl. tax)"])}')
        # print(f'Total Tax {len(self._df["Tax"])}')
        # print(f'Total Availability {len(self._df["Availability"])}')
        # print(f'Total Number of reviews {len(self._df["Number of reviews"])}')
        # print("--------------------------------------")
                
        # Saving to csv file
        self._save_to_csv("Books")
        driver.quit()
        
        


# Implementation
DRIVER_PATH = "chromedriver_win32/chromedriver.exe"
pages_to_scrape = 5

scraper = Scraper(DRIVER_PATH, pages_to_scrape)
scraper.scrape()
            
        

