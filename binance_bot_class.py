import asyncio
from binance.async_client import AsyncClient
from binance.enums import *
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

class BinanceBot:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.client = None
        self.account_balances = {} 
        self.tickers_info = []  # dict리스트. dict하나에 티커의 정보 (현재가, rsi, 최근 80일간 최고점, 최저점 대비 현재가가 몇 % 에 있는지지)
        self.symbol_list = ["CRVUSDT","CHRUSDT","RUNEUSDT","ARUSDT","FARTCOINUSDT"]

    async def initialize_client(self):
        self.client = await AsyncClient.create(self.api_key, self.api_secret)

    async def ticker_info(self, symbol):
        try:
            ticker = await self.client.futures_symbol_ticker(symbol=symbol)
            return ticker
        except Exception as e:
            print(f"Error fetching ticker info for {symbol}: {e}")

    async def futures_historical_klines(self,symbol,interval,start_str,end_str):
        try:
            data = await self.client.futures_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_str,
            end_str=end_str)
            return data
        except Exception as e:
            print(f"Error fetching historical_klines for {symbol}: {e}")

    async def update_avbl_balances(self):
        try:
            account_info = await self.client.futures_account()
            balances = account_info['assets']
            self.account_balances = {balance['asset']: float(balance['availableBalance']) for balance in balances if float(balance['availableBalance']) > 0}
        except Exception as e:
            print(f"Error fetching futures balance: {e}")


    async def order_market_buy(self, symbol, quantity):
        try:
            order = await self.client.order_market_buy(symbol=symbol, quantity=quantity)
            return order
        except Exception as e:
            print(f"Error placing order for {symbol}: {e}")
    
    async def execute_strategy(self,symbol):
        pass

    async def close(self):
        await self.client.close_connection()