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

from chapter05.utils import KiwoomTR
from chapter06.config import websocket_url


class WebSocketClient:
	def __init__(self, uri):
		self.uri = uri
		self.websocket = None
		self.connected = False
		self.keep_running = True
		kiwoom_tr = KiwoomTR()
		self.token = kiwoom_tr.token

	# WebSocket 서버에 연결합니다.
	async def connect(self):
		try:
			self.websocket = await websockets.connect(self.uri)
			self.connected = True
			print("서버와 연결을 시도 중입니다.")

			# 로그인 패킷
			param = {
				'trnm': 'LOGIN',
				'token': self.token
			}

			logger.info('실시간 시세 서버로 로그인 패킷을 전송합니다.')
			# 웹소켓 연결 시 로그인 정보 전달
			await self.send_message(message=param)

		except Exception as e:
			logger.info(f'Connection error: {e}')
			self.connected = False

	# 서버에 메시지를 보냅니다. 연결이 없다면 자동으로 연결합니다.
	async def send_message(self, message):
		if not self.connected:
			await self.connect()  # 연결이 끊어졌다면 재연결
		
		# 연결 상태와 websocket 객체 확인
		if not self.connected or self.websocket is None:
			logger.error("WebSocket 연결이 없습니다. 메시지를 보낼 수 없습니다.")
			return False
		
		try:
			# message가 문자열이 아니면 JSON으로 직렬화
			if not isinstance(message, str):
				message = json.dumps(message)

			await self.websocket.send(message)
			print(f'Message sent: {message}')
			return True
		except Exception as e:
			logger.error(f"메시지 전송 실패: {e}")
			self.connected = False
			return False

	# 서버에서 오는 메시지를 수신하여 출력합니다.
	async def receive_messages(self):
		while self.keep_running:
			try:
				# websocket 연결 확인
				if not self.connected or self.websocket is None:
					logger.error("WebSocket 연결이 없습니다. 수신을 중단합니다.")
					break
				
				# 서버로부터 수신한 메시지를 JSON 형식으로 파싱
				response = json.loads(await self.websocket.recv())
				tr_name = response.get('trnm')

				# 메시지 유형이 LOGIN일 경우 로그인 시도 결과 체크
				if tr_name == 'LOGIN':
					if response.get('return_code') != 0:
						logger.info('로그인 실패하였습니다. : ', response.get('return_msg'))
						await self.disconnect()
					else:
						logger.info('로그인 성공하였습니다.')
				# 메시지 유형이 PING일 경우 수신값 그대로 송신
				elif tr_name == 'PING':
					await self.send_message(response)
				# 메시지 유형이 REAL일 경우 실시간 체결과 호가 수신
				elif tr_name == 'REAL':
					for chunk_data_info_map in response.get('data', []):
						종목코드 = chunk_data_info_map['item'].replace('_AL', '').replace('A', '')
						if chunk_data_info_map['name'] == '주식체결결':	# ;name' 또는 'type'으로 구분하여 접근
							tick_info_map = chunk_data_info_map['values']
							체결시간 = tick_info_map['20']
							현재가 = abs(int(tick_info_map['10']))	 # 중간가 주문으로 인해 소수점 현재가 발생할 수 있음
							전일대비 = float(tick_info_map['11'])
							등락율 = float(tick_info_map['12'])
							체결량 = int(tick_info_map['15'])	# +는 매수체결, -는 매도체결
							logger.info(
								f'종목코드: {종목코드}, '
								f'체결시간: {체결시간}, '
								f'현재가: {현재가}, '
								f'전일대비: {전일대비}, '
								f'등락율: {등락율}, '
								f'체결량: {체결량}'
							)
							# await self.remove_realtime_group(group_num='1')	 # 실시간 체결 데이터 획득 이후 실시간 해지
						elif chunk_data_info_map['name'] == '주식호가잔량량':
							ask_info_map = chunk_data_info_map['values']
							호가시간 = ask_info_map['21']
							매도호가1 = abs(int(ask_info_map['41']))
							매도호가수량1 = int(ask_info_map['61'])
							매수호가1 = abs(int(ask_info_map['51']))
							매수호가수량1 = int(ask_info_map['71'])
							logger.info(
								f'종목코드: {종목코드}, '
								f'호가시간: {호가시간}, '
								f'매도호가1: {매도호가1}, '
								f'매도호가수량1: {매도호가수량1}, '
								f'매수호가1: {매수호가1}, '
								f'매수호가수량1: {매수호가수량1}'
							)
				else:
					logger.info(f'실시간 시세 서버 응답 수신: {response}')

			except websockets.exceptions.ConnectionClosed:
				logger.info('Connection closed by the server')
				self.connected = False
				await self.websocket.close()

	async def remove_realtime_group(self, group_num='1'):
		logger.info(f"그룹번호: {group_num} 실시간 등록 해지!")
		await self.send_message({
			'trnm': 'REMOVE', # 서비스명
			'grp_no': group_num, # 그룹번호
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
			logger.info('Disconnected from WebSocket server')

async def main():
	# WebSocketClient 전역 변수 선언
	websocket_client = WebSocketClient(websocket_url)

	# WebSocket 클라이언트를 백그라운드에서 실행합니다.
	receive_task = asyncio.create_task(websocket_client.run())

	# 연결 대기 (최대 5초)
	await asyncio.sleep(2)
	
	# 연결 상태 확인
	if not websocket_client.connected or websocket_client.websocket is None:
		logger.error("WebSocket 연결 실패. 프로그램을 종료합니다.")
		websocket_client.keep_running = False
		receive_task.cancel()
		return

	logger.info("WebSocket 연결 성공. 실시간 등록을 시작합니다.")
	
	# 실시간 항목 등록
	success = await websocket_client.send_message({ 
		'trnm': 'REG', # 서비스명 (REG: 등록, REMOVE: 해제)
		'grp_no': '1', # 그룹번호
		'refresh': '1', # 기존등록유지여부
		'data': [{ # 실시간 등록 리스트
			'item': ['005930_AL', '039490_AL'], # 실시간 등록 요소 (삼성전자, 키움증권 SOR 시세 등록)
			'type': ['0B', '0D'], # 실시간 항목 (주식 체결, 호가 등록)
		}]
	})
	
	if not success:
		logger.error("실시간 등록 실패. 프로그램을 종료합니다.")
		websocket_client.keep_running = False
		receive_task.cancel()
		return

	# 수신 작업이 종료될 때까지 대기
	try:
		await receive_task
	except asyncio.CancelledError:
		logger.info("수신 작업이 취소되었습니다.")
	finally:
		await websocket_client.disconnect()

# asyncio로 프로그램을 실행합니다.
if __name__ == '__main__':
	asyncio.run(main())
