import asyncio

# 공유 변수 (공통 데이터)
shared_data = {
    "ticker_info": 0,  # 티커 정보
    "balance_info": 0  # 잔고 정보
}

# 락 객체: 데이터 갱신 중 다른 작업이 끼어들지 못하도록 보호
data_lock = asyncio.Lock()

# 티커 정보를 갱신하는 함수 (5초마다)
async def update_ticker():
    while True:
        async with data_lock:  # 데이터 갱신 시 락 사용
            shared_data["ticker_info"] += 1  # 예시 데이터
            print("[Ticker] Updated ticker_info:", shared_data["ticker_info"])
        await asyncio.sleep(3)  # 5초 대기

# 잔고 정보를 갱신하는 함수 (3초마다)
async def update_balance():
    while True:
        async with data_lock:  # 데이터 갱신 시 락 사용
            shared_data["balance_info"] += 2 # 예시 데이터
            print("[Balance] Updated balance_info:", shared_data["balance_info"])
        await asyncio.sleep(5)  # 3초 대기

# 매수 조건을 판단하고 매수를 실행하는 함수
async def execute_trade():
    while True:
        async with data_lock:  # 데이터 읽기 시에도 락 사용
            ticker = shared_data["ticker_info"]
            balance = shared_data["balance_info"]

            # 데이터가 모두 갱신된 후에 조건 체크
            if ticker and balance:
                if ticker > 5 :
                    shared_data["ticker_info"] = 0
                    print('short!!')
                if balance > 8 :
                    shared_data["balance_info"] = 0
                    print("earning!!")
            else:
                print("[Trade] Waiting for data to initialize...")

        await asyncio.sleep(1)  # 2초마다 매수 조건 확인

# 메인 실행 함수
async def main():
    # 각각의 비동기 작업 실행
    await asyncio.gather(
        update_ticker(),
        update_balance(),
        execute_trade()
    )

if __name__ == "__main__":
    asyncio.run(main())
