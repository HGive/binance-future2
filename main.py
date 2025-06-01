import os
import time
import traceback
from dotenv import load_dotenv
from binance.client import Client
from classes.shared_data import SharedData
from classes.chart_data_manager import ChartDataManager

load_dotenv()

def main():
    client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"))

    shared_data = SharedData()
    chart_manager = ChartDataManager(client, "BTCUSDT", Client.KLINE_INTERVAL_1HOUR, shared_data)

    # 초기 데이터 로드
    chart_manager.initialize_data()

    while True:
        try:
            chart_manager.update_latest_candle()
        except Exception:
            print("[차트 업데이트 오류]")
            traceback.print_exc()

        time.sleep(60)  # 1분마다 반복


if __name__ == "__main__":
    main()
