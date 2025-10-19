import requests
import time
from config import api_key, api_secret_key, host

# 접근토큰 발급
def fn_au10001(data):
    # 1. 요청할 API URL
    endpoint = "/oauth2/token"
    url = host + endpoint

    # 2. header 데이터
    headers = {
        "Content-Type": "application/json;charset=UTF-8", # 컨텐츠타입
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    response.raise_for_status()  # 요청 실패 시 예외 발생

    # print("Code:", response.status_code)
    # print("Header:", json.dumps({key: response.headers.get(key) for key in ["next-key", "cont-yn", "api-id"]}, indent=4, ensure_ascii=False))
    # print("Body:", json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력
    print(response.json()["token"])

    return response.json()["token"]


# 종목정보 리스트
def fn_ka10099(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    endpoint = '/api/dostk/stkinfo'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'ka10099', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    try:
        response.raise_for_status()  # 요청 실패 시 예외 발생
    except requests.HTTPError as e:
        # 에러를 response 내용까지 추가해서 출력
        error_message = f'HTTP Error : {e}\nResponse Body : {response.text} - {e.response.text}'
        raise requests.HTTPError(error_message) from e
    
    return response.json()['list']


# 실행 구간
if __name__ == "__main__":

    # 1. 요청 데이터
    params = {
        "grant_type": "client_credentials",  # grant_type
        "appkey": api_key,  # 앱키
        "secretkey": api_secret_key  # 시크릿키
    }

    # 2. API 실행
    token = fn_au10001(data=params)
    # 토큰 출력
    print("Access Token:", token)

    # 3. 요청 데이터
    params = {
        "mrkt_tp": "0"  # 0:코스피,10:코스닥,3:ELW,8:ETF,30:K-OTC,50:코넥스,5:신주인수권,4:뮤추얼펀드,6:리츠,9:하이일드
    }

    # 5. API 실행
    kospi_stock_info_list = fn_ka10099(token=token, data=params)
    print(kospi_stock_info_list)

    time.sleep(1)  # TR 요청 제한을 피하기 위해 1초 대기

    # 6. 요청 데이터
    params = {
        "mrkt_tp": "10"  # 시장구분 0:코스피, 10:코스닥, 3:ETF, 8:ELW, 30:K-OTC, 50:코넥스, 5:신주인수권, 4:뮤추얼펀드, 6:리츠, 9:하이일드
    }

    # 7. API 실행
    kosdaq_stock_info_list = fn_ka10099(token=token, data=params)
    print(kosdaq_stock_info_list)

    print(f"KOSPI  종목수 : {len(kospi_stock_info_list)}")
    print(f"KOSDAQ 종목수 : {len(kosdaq_stock_info_list)}")
