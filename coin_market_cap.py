import requests
from bs4 import BeautifulSoup
import json

class CoinMarketCap:
    def __init__(self):
        self.base_url = 'https://coinmarketcap.com/currencies/'

    def fetch_page(self, coin_acronym):
        """Fetches the HTML content of the given cryptocurrency's page."""
        url = f'{self.base_url}{coin_acronym}/'
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def parse_data(self, html_content):
        """Parses the HTML content to extract relevant data."""
        soup = BeautifulSoup(html_content, 'html.parser')
        data = {}

        # Extract the price (example selector; should be adjusted based on the actual site structure)
        price_tag = soup.find('div', class_='priceValue')
        if price_tag:
            data['price'] = price_tag.text.strip()
        else:
            data['price'] = 'N/A'

        # Extract the market cap (example selector; should be adjusted based on the actual site structure)
        market_cap_tag = soup.find('div', class_='statsValue')
        if market_cap_tag:
            data['market_cap'] = market_cap_tag.text.strip()
        else:
            data['market_cap'] = 'N/A'

        # Additional data extraction can be added here

        return data

    def get_coin_data(self, coin_acronym):
        """Gets the data for a single cryptocurrency."""
        html_content = self.fetch_page(coin_acronym)
        if html_content:
            return self.parse_data(html_content)
        else:
            return {'error': f'Could not retrieve data for {coin_acronym}'}

    def get_coins_data(self, acronyms):
        """Gets the data for a list of cryptocurrencies."""
        results = {}
        for acronym in acronyms:
            results[acronym] = self.get_coin_data(acronym.lower())
        return results

    def get_coins_data_json(self, acronyms):
        """Returns the data for a list of cryptocurrencies in JSON format."""
        data = self.get_coins_data(acronyms)
        return json.dumps(data, indent=4)

# Example usage
if __name__ == "__main__":
    coin_market_cap = CoinMarketCap()
    acronyms = ['bitcoin', 'ethereum']
    print(coin_market_cap.get_coins_data_json(acronyms))
