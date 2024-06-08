from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CoinRequestSerializer
import requests
from bs4 import BeautifulSoup
from .coin_market_cap import CoinMarketCap

class CoinDataView(APIView):
    def post(self, request):
        serializer = CoinRequestSerializer(data=request.data)
        if serializer.is_valid():
            acronyms = serializer.validated_data['acronyms']
            coin_data = self.get_coin_data(acronyms)
            return Response(coin_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_coin_data(self, acronyms):
        data = {}
        for acronym in acronyms:
            url = f'https://coinmarketcap.com/{acronym}'  # Replace with the actual URL
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                price = soup.find('span', {'class': 'price'}).text  # Adjust the selector as needed
                data[acronym] = {'price': price}
            else:
                data[acronym] = {'error': 'Could not retrieve data'}
        return data
# In coins/views.py

class CoinDataView(APIView):
    def post(self, request):
        serializer = CoinRequestSerializer(data=request.data)
        if serializer.is_valid():
            acronyms = serializer.validated_data['acronyms']
            coin_market_cap = CoinMarketCap()
            coin_data_json = coin_market_cap.get_coins_data_json(acronyms)
            return Response(json.loads(coin_data_json), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
