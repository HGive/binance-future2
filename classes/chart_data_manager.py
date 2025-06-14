import pandas as pd
from binance.client import Client
from datetime import datetime

class ChartDataManager:
    def __init__(self, client: Client, interval: str, shared_state):
        self.client = client
        self.interval = interval
        self.shared_state = shared_state
        self.max_len = 50

    def initialize_data(self, symbol: str,):
        klines = self.client.get_klines(symbol=symbol, interval=self.interval, limit=self.max_len)
        df = pd.DataFrame(klines, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
        ])
        df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
        df.set_index("open_time", inplace=True)
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)
        df["row_num"] = range(1, len(df) + 1)
        self.shared_state.chart_data[symbol] = df
        print(f"[{symbol}] 초기 차트 데이터 로드 완료 ({len(df)}개)")

    def update_latest_candle(self, symbol: str):
        latest = self.client.get_klines(symbol=symbol, interval=self.interval, limit=1)[0]
        open_time = pd.to_datetime(latest[0], unit='ms')

        df = self.shared_state.chart_data.get(symbol)
        if df is None:
            print(f"[{symbol}] 초기화가 먼저 필요합니다.")
            return

        if open_time not in df.index:
            new_row = {
                "open": float(latest[1]),
                "high": float(latest[2]),
                "low": float(latest[3]),
                "close": float(latest[4]),
                "volume": float(latest[5]),
                "row_num": df["row_num"].max() + 1
            }
            df.loc[open_time] = new_row
            if len(df) > self.max_len:
                df = df.iloc[1:]
            self.shared_state.chart_data[symbol] = df
            print(f"[{symbol}] 새로운 봉 추가됨: {open_time}")
        else:
            print(f"[{symbol}] 이미 최신 봉 반영됨: {open_time}")
