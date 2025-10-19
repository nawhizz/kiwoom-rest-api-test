import requests
import json
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

    return response.json()["token"]


# 실행 구간
if __name__ == "__main__":
    # 1. 요청 데이터
    params = {
        "grant_type": "client_credentials",  # grant_type
        "appkey": api_key,  # 앱키
        "secretkey": api_secret_key  # 시크릿키
    }

    # 2. API 실행
    access_token = fn_au10001(data=params)
    # 토큰 출력
    print("Access Token:", access_token)