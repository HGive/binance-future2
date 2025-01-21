from binance_bot_class import BinanceBot
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

async def main():
    API_KEY = os.getenv("BINANCE_API_KEY")
    API_SECRET = os.getenv("BINANCE_API_SECRET")
    SYMBOL = "BTCUSDT"
    INITIAL_QTY = 0.001  # Example amount
    DIP_PERCENTAGE = 5  # Example: Buy if price drops 5%
    MAX_ADDITIONAL_ORDERS = 2  # Total of 3 buys (initial + 2 additional)

    bot = BinanceBot(API_KEY, API_SECRET)
    await bot.initialize_client()

    try:
        future_balance = await bot.get_future_balance()
        print("Futures USDT Balance:", future_balance)
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
