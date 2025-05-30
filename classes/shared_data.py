class SharedData:
    def __init__(self):
        self.chart_data = {}  # symbol별 차트 DataFrame 저장: ex) {"BTCUSDT": pd.DataFrame()}
