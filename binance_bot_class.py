import asyncio
from binance.async_client import AsyncClient
from binance.enums import *

class BinanceBot:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = None

    async def initialize_client(self):
        self.client = await AsyncClient.create(self.api_key, self.api_secret)

    async def get_future_balance(self):
        try:
            account_info = await self.client.futures_account()
            balances = account_info['assets']
            return {balance['asset']: float(balance['availableBalance']) for balance in balances if float(balance['availableBalance']) > 0}
        except Exception as e:
            print(f"Error fetching futures balance: {e}")

    async def get_market_price(self, symbol):
        try:
            ticker = await self.client.get_ticker(symbol=symbol)
            return float(ticker['lastPrice'])
        except Exception as e:
            print(f"Error fetching market price for {symbol}: {e}")

    async def place_order(self, symbol, quantity, order_type=ORDER_TYPE_MARKET):
        try:
            if order_type == ORDER_TYPE_MARKET:
                order = await self.client.order_market_buy(symbol=symbol, quantity=quantity)
                return order
        except Exception as e:
            print(f"Error placing order for {symbol}: {e}")

    async def execute_strategy(self, symbol, initial_qty, dip_percentage, max_additional_orders):
        try:
            balance = await self.get_balance()
            if symbol[:-4] not in balance:
                print(f"No balance for {symbol[:-4]}. Starting initial purchase.")
                await self.place_order(symbol, initial_qty)

            for i in range(max_additional_orders):
                await asyncio.sleep(60 * 60 * 24)  # Simulating daily candle wait
                market_price = await self.get_market_price(symbol)
                last_order_price = market_price / ((100 - dip_percentage) / 100)**(i + 1)

                if market_price <= last_order_price:
                    additional_qty = initial_qty / 2 ** (i + 1)
                    print(f"Placing additional buy order: {additional_qty} of {symbol}")
                    await self.place_order(symbol, additional_qty)

        except Exception as e:
            print(f"Error executing strategy: {e}")

    async def close(self):
        await self.client.close_connection()