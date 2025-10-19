"""
키움증권 REST API / WebSocket 예제 패키지

이 패키지는 키움증권의 REST API와 WebSocket을 활용한 
주식 자동매매 및 실시간 데이터 수신 예제를 제공합니다.
"""

__version__ = "1.0.0"
__author__ = "nawhizz"
__email__ = "nawhizz@gmail.com"

# 주요 클래스들을 패키지 레벨에서 import 가능하도록 설정
from .chapter05.utils import KiwoomTR

__all__ = [
    'KiwoomTR',
]
