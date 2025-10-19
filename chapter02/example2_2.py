import requests
import datetime
import pandas as pd
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


# 일별주가요청
def fn_ka10086(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    endpoint = '/api/dostk/mrkcond'
    url =  host + endpoint

	# 2. header 데이터
    headers = {
		'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
		'authorization': f'Bearer {token}', # 접근토큰
		'cont-yn': cont_yn, # 연속조회여부
		'next-key': next_key, # 연속조회키
		'api-id': 'ka10086', # TR명
	}

	# 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    try:
        response.raise_for_status()  # 요청 실패 시 예외 발생
    except requests.HTTPError as e:
        # 에러를 response 내용까지 추가해서 출력
        error_message = f'HTTP Error : {e}\nResponse Body : {response.text} - {e.response.text}'
        raise requests.HTTPError(error_message) from e
    
    res = response.json()['daly_stkpc']
    df = pd.DataFrame(res)
    df = df[::-1].reset_index(drop=True)
    for column_name in ["open_pric", "high_pric", "low_pric", "close_pric"]:
        df[column_name] = df[column_name].apply(lambda x: abs(int(x)))

    column_name_to_kor_name_map = {
        "date": "날짜",
        "open_pric": "시가",
        "high_pric": "고가",
        "low_pric": "저가",
        "close_pric": "종가",
        "pred_rt": "전일비",
        "flu_rt": "등락률",
        "trde_qty": "거래량",
        "amt_mn": "금액(백만)",
        "crd_rt": "신용비",
        "ind": "개인",
        "orgn": "기관",
        "for_qty": "외인수량",
        "frgn": "외국계",
        "prm": "프로그램",
        "for_rt": "외인비",
        "for_poss": "외인보유",
        "for_wght": "외인비중",
        "for_netprps": "외인순매수",
        "orgn_netprps": "기관순매수",
        "ind_netprps": "개인순매수",
        "crd_remn_rt": "신용잔고율"
    }

    df.rename(columns=column_name_to_kor_name_map, inplace=True)
    return df


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
		'stk_cd': '005930_AL', # 종목코드 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
		'qry_dt': datetime.datetime.now().strftime('%Y%m%d'), # 조회일자 YYYYMMDD
		'indc_tp': '0', # 표시구분 0:수량, 1:금액(백만원)
	}

    # 4. API 실행
    df = fn_ka10086(token=token, data=params)
    print(df.to_string())
