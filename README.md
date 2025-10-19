# YouTube 주식코딩 강의 예제 코드

## 키움증권 REST API / Websocket 예제

## Python 3.10 버전 Anaconda 환경 사용

### 환경 설정 방법-자세한 내용은 영상 참고

1. anaconda prompt 열기
2. conda create -n kiwoom_rest_api python=3.10
3. PyCharm 에서 kiwoom_rest_api Interpreter 설정
4. 프로젝트 경로에서 pip install -r requirements.txt

### 강의 순서

1. 기존 Open AP1+ 비교 / 파이썬 개발 환경 설정 / API KEY 발급 / 로그인
2. 기본 TR 요청 - 종목코드 리스트, 계좌 정보, 일봉
3. 주문 요청 - 시장가, 지정가 매수/매도 주문 (feat NXT. SOR 주문)
4. TR 요청과 연속 조회 - 계좌 정보, 일봉 기준 연속 데이터 조회 (feat. TR 요청 제한)
5. REST API TR 요청 동합 스크립트 utils.py (분봉, 등락률 상위 TR 추가)
6. 웹소켓 실시간 데이터 - 주식 체결, 호가 데이터 (실시간 등록, 해제) / 실시간 주문 접수 및 체결
7. 웹소켓 실시간 데이터 - 조건검색식 연동 (조건식 일반 조회, 실시간 등록, 실시간 해제)
8. 통합 프로그램 예제 - 조건검색식 기반 매수 / 매도 / 스탑로스 / 트레일링 스탑 (feat. 멀티프로세싱, PyQt)

