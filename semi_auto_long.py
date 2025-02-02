from binance_bot_class import BinanceBot
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

async def main():

    bot = BinanceBot()
    await bot.initialize_client()

    # 각각의 비동기 작업 실행
    await bot.update_tickers(),
    await bot.update_avbl_balances(),
    await bot.execute_strategy()

if __name__ == "__main__":
    asyncio.run(main())
