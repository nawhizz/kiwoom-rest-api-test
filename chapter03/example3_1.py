import time

import requests
from config import api_key, api_secret_key, host

# 접근토큰 발급
def fn_au10001(data):
    # 1. 요청할 API URL
    endpoint = '/oauth2/token'
    url = host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    response.raise_for_status()  # 요청 실패 시 예외 발생

    # print('Code:', response.status_code)
    # print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    # print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력
    print(response.json()['token'])

    return response.json()['token']


#주식 매수주문
def fn_kt10000(token, data, cont_yn='N', next_key=''):
    endpoint = '/api/dostk/ordr'
    url = host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt10000', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)
    
    try:
        response.raise_for_status()  # 요청 실패 시 예외 발생
    except requests.HTTPError as e:
        # 에러를 response 내용까지 추가해서 출력
        error_message = f'HTTP Error: {e}\nResponse Body: {response.text}'
        raise requests.HTTPError(error_message) from e
    
    # 응답 데이터 확인 및 안전한 처리
    res = response.json()
    print(f"매수주문 응답: {res}")
    
    # ord_no가 있는지 확인
    if 'ord_no' in res:
        return res['ord_no']
    else:
        print(f"⚠️ 주문번호가 응답에 없습니다. 응답: {res}")
        return None


#주식 매도주문
def fn_kt10001(token, data, cont_yn='N', next_key=''):
    endpoint = '/api/dostk/ordr'
    url = host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt16901', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    try:
        response.raise_for_status()  # 요청 실패 시 예외 발생
    except requests.HTTPError as e:
        # 에러를 response 내용까지 추가해서 출력
        error_message = f'HTTP Error: {e}\nResponse Body: {response.text}'
        raise requests.HTTPError(error_message) from e
    
    # 응답 데이터 확인 및 안전한 처리
    res = response.json()
    print(f"매도주문 응답: {res}")
    
    # ord_no가 있는지 확인
    if 'ord_no' in res:
        return res['ord_no']
    else:
        print(f"⚠️ 주문번호가 응답에 없습니다. 응답: {res}")
        return None


#주식 정정주문
def fn_kt10002(token, data, cont_yn='N', next_key=''):
    endpoint = '/api/dostk/ordr'
    url = host + endpoint
    
    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt10002', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    try:
        response.raise_for_status()  # 요청 실패 시 예외 발생
    except requests.HTTPError as e:
        # 에러를 response 내용까지 추가해서 출력
        error_message = f'HTTP Error: {e}\nResponse Body: {response.text}'
        raise requests.HTTPError(error_message) from e
    
    # 응답 데이터 확인 및 안전한 처리
    res = response.json()
    print(f"정정주문 응답: {res}")
    
    # ord_no가 있는지 확인
    if 'ord_no' in res:
        return res['ord_no']
    else:
        print(f"⚠️ 주문번호가 응답에 없습니다. 응답: {res}")
        return None


# 주식 취소주문
def fn_kt10003(token, data, cont_yn='N', next_key=''):
    endpoint ='/api/dostk/ordr' 
    url = host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt10003', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    try:
        response.raise_for_status()  # 요청 실패 시 예외 발생
    except requests.HTTPError as e:
        # 에러를 response 내용까지 추가해서 출력
        error_message = f"HTTP Error: {e}\nResponse Body: {response.text}"
        raise requests.HTTPError(error_message) from e
    
    # 응답 데이터 확인 및 안전한 처리
    res = response.json()
    print(f"취소주문 응답: {res}")
    
    # ord_no가 있는지 확인
    if 'ord_no' in res:
        return res['ord_no']
    else:
        print(f"⚠️ 주문번호가 응답에 없습니다. 응답: {res}")
        return None


# 실행 구간
if __name__ == '__main__':
    #1. 요청 데이터
    params = {
        'grant_type': 'client_credentials', # granttype
        'appkey': api_key, # 앨키
        'secretkey': api_secret_key, # 시크릿키
    }

    # 2. API 실행
    token = fn_au10001(data=params)

    # 매수주문 요청 데이터
    params = {
		'dmst_stex_tp': 'KRX', # 국내거래소구분 KRX,NXT,SOR
		'stk_cd': '005930', # 종목코드 
		'ord_qty': '1', # 주문수량 
		'ord_uv': '', # 주문단가  # 시장기 주문일 경우 공백  # NXT는 시장가 불가능
		'trde_tp': '3', # 매매구분 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)
		'cond_uv': '', # 조건단가 
	}

    # 3. API 실행 (매수주문)
    print("=== 매수주문 실행 ===")
    buy_order_num = fn_kt10000(token=token, data=params)
    
    if buy_order_num is None:
        print("❌ 매수주문 실패 - 다음 단계를 건너뜁니다.")
        exit()

    # 매도주문 요청 데이터
    params = {
		'dmst_stex_tp': 'KRX', # 국내거래소구분 KRX,NXT,SOR
		'stk_cd': '005930', # 종목코드 
		'ord_qty': '1', # 주문수량 
		'ord_uv': '65000', # 주문단가  # 시장기 주문일 경우 공백  # NXT는 시장가 불가능
		'trde_tp': '0', # 매매구분 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)
		'cond_uv': '', # 조건단가 
	}

    # 4. API 실행 (매도주문)
    print("\n=== 매도주문 실행 ===")
    sell_order_num = fn_kt10001(token=token, data=params)
    
    if sell_order_num is None:
        print("❌ 매도주문 실패 - 정정/취소 단계를 건너뜁니다.")
        exit()

    # 정정주문 요청 데이터
    params = {
		'dmst_stex_tp': 'KRX', # 국내거래소구분 KRX,NXT,SOR
        'orig_ord_no': sell_order_num, # 원주문번호
		'stk_cd': '005930', # 종목코드 
		'mdfy_qty': '1', # 정정수량 
		'mdfy_uv': '60000', # 정정단가
		'mdfy_cond_uv': '', # 정정조건단가 
	}

    # 5. API 실행 (정정주문)
    print("\n=== 정정주문 실행 ===")
    modify_order_num = fn_kt10002(token=token, data=params)
    
    if modify_order_num is None:
        print("❌ 정정주문 실패 - 취소 단계를 건너뜁니다.")
        exit()

   # 취소주문 요청 데이터
    params = {
		'dmst_stex_tp': 'KRX', # 국내거래소구분 KRX,NXT,SOR
        'orig_ord_no': modify_order_num, # 원주문번호
		'stk_cd': '005930', # 종목코드 
		'cncl_qty': '0', # 취소수량 '0' 입력시 잔량 전부 취소
	}

    # 6. API 실행 (취소주문)
    print("\n=== 취소주문 실행 ===")
    cancel_result = fn_kt10003(token=token, data=params)
    
    if cancel_result is None:
        print("❌ 취소주문 실패")
    else:
        print("✅ 모든 주문 테스트 완료")
