# coins/coinmarketcap.py
# coins/coinmarketcap.py
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class CoinMarketCap:
    BASE_URL = 'https://coinmarketcap.com/currencies/'

    def __init__(self):
        self.options = Options()
        self.options.headless = True  # Run in headless mode
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def scrape_coin_data(self, coin_acronym):
        url = f"{self.BASE_URL}{coin_acronym}/"
        self.driver.get(url)
        
        try:
            price_element = self.driver.find_element(By.XPATH, "//div[@class='priceValue ']/span")
            price = price_element.text
        except Exception as e:
            price = None
        
        return {"coin": coin_acronym, "price": price}
    
    def get_crypto_data(self, coin_acronyms):
        results = []
        for coin in coin_acronyms:
            data = self.scrape_coin_data(coin)
            results.append(data)
        self.driver.quit()
        return results
