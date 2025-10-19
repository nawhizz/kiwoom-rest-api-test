import asyncio 
import websockets
import json
import sys
import os

from loguru import logger

# 프로젝트 루트를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from chapter07.config import api_key, api_secret_key, host, websocket_url
from chapter05.utils import KiwoomTR


class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.connected = False
        self.keep_running = True
        kiwoom_tr = KiwoomTR()
        self.token = kiwoom_tr.token
        self.condition_name_to_idx_dict = dict()  # 조건검색식의 인덱스 값을 저장할 딕셔너리
        self.target_condition_name = "매수테스트"   # '매수테스트'라는 이름으로 된 조건식의 검색 결과와 실시간 편입/편출 등록을 할 것임

    # Websocket 서버에 연결합니다.
    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            logger.info("서버와 연결을 시도 중입니다.")
            
            #로그인 패릿
            param = {
                'trnm': "LOGIN",
                'token': self.token
            }

            logger.info('실시간 시세 서버로 로그인 패킷을 전송합니다.')
            # 웹소켓 연결 시 로그인 점보 전달
            await self.send_message(message=param)

        except Exception as e:
            logger.info(f'Connection error: {e}')
            self.connected = False

    # 서버에 메시지를 보냅니다. 연결이 없다면 자동으로 연결합니다.
    async def send_message(self, message):
        if not self.connected:
            await self.connect() #연결이 끊어졌다면 재연결
        if self.connected:
            # message가 문자열이 아니면 JSON으로 직렬화
            if not isinstance(message, str):
                message = json.dumps(message)

            await self.websocket.send(message)
            logger.info(f'Message sent. Message: {message}')

    # 서버에서 오는 메시지를 수신하여 출력합니다.
    async def receive_messages(self):
        while self.keep_running:
            try:
                # 서버로부터 수신한 메시지를 JSON 청식으로 파싱
                response = json.loads(await self.websocket.recv())
                tr_name = response.get("trnm")
                # 메시지 유형이 L0GIN일 경우 로그인 시도 결과 체크
                if tr_name == "LOGIN":
                    if response.get("return_code") != 0:
                        logger.info('로그인 실패하였습니다. : ', response.get("return_msg"))
                        await self.disconnect()
                    else:
                        logger.info('로그인 성공하였습니다.')
                elif tr_name == "PINE":
                    await self.send_message(response) # 메시지 유형이 PING일 경우 수신값 그대로 송신
                elif tr_name == "CNSRLST": # 조건검색식 리스트 수신
                    for condition_idx, condition_name in response.get("data", []):
                        logger.info(f"조건식 index: {condition_idx}, 조건명: {condition_name}")
                        self.condition_name_to_idx_dict[condition_name] = condition_idx # 조건식 index를 활용해서 조건식 결과 조회 요청
                        if condition_name == self.target_condition_name:
                            await self.req_condition_general_result(condition_name)
                elif tr_name == "CNSRREQ": # 조건검색 요청 일반 결과 수신
                    logger.info(f'결과: {response}')
                    for per_stock_info_map in response.get("data", []):
                        종목코드 = per_stock_info_map['9001'].replace("_AL", "").replace("A", "")
                        종목명 = per_stock_info_map['302']
                        현재가 = per_stock_info_map['10']
                        전일대비기호 = per_stock_info_map['25']
                        전일대비 = per_stock_info_map['11']
                        등락율 = per_stock_info_map['12']
                        누적거래량 = per_stock_info_map['13']
                        시가 = per_stock_info_map['16']
                        고가 = per_stock_info_map['17']
                        저가 = per_stock_info_map['18']
                        logger.info(
                            f"종목코드: {종목코드}, "
                            f"종목명: {종목명}, "
                            f"현재가: {현재가}, "
                            f"전일대비기호: {전일대비기호}, "
                            f"전일대비: {전일대비} ,"
                            f"등락율: {등락율}, "
                            f"누적거래량: {누적거래량}, "
                            f"시가: {시가}, "
                            f"고가: {고가}, "
                            f"저가: {저가}"
                        )
                else:
                    logger.info(f'실시간 시세 서버 응답 수신: {response}')

            except websockets.exceptions.ConnectionClosed:
                logger.info('Connection closed by the server')
                self.connected = False
                await self.websocket.close()

    async def req_condition_general_result(self, condition_name):
        condition_idx = self.condition_name_to_idx_dict[condition_name]
        logger.info(f"{condition_name} 조건 검색 결과 조회")
        await self.send_message({
            'trnm': 'CNSRREQ',  # 서비스명
            'seq': f'{condition_idx}',  # 조건검색식 일련번호
            'search_type': '0',  # 조회타입
            'stex_tp': 'K',  # 거래소구분
            'cont_yn': 'N',  # 연속조회여부
            'next_key': '',  # 연속조회키
        })

    # WebSocket 실행
    async def run(self):
        await self.connect()
        await self.receive_messages()

    # WebSocket 연결 종료
    async def disconnect(self):
        self.keep_running = False
        if self.connected and self.websocket:
            await self.websocket.close()
            self.connected = False
            logger.info( 'Disconnected from WebSocket server')

async def main():
    # WebSocketClient 전역 변수 선언
    websocket_client = WebSocketClient(websocket_url)

    # WebSocket 클라이언트를 그라운드에서 실행합니다.
    receive_task = asyncio.create_task(websocket_client.run())

    #실시간 목등록
    await asyncio.sleep(1)
    await websocket_client.send_message({
        'trnm': 'CNSRLST',  # TR명명
    })

    #수신 작업 종료될 때까지 대기
    await receive_task

# asyncio로 프로그램을 실행합니다.
if __name__ == '__main__':
    asyncio.run(main())
