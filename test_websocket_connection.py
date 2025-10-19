#!/usr/bin/env python3
"""
WebSocket 연결 테스트 스크립트
"""

import asyncio
import websockets
import sys
import os

# 프로젝트 루트를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# WebSocket URL 직접 설정
websocket_url = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"

async def test_websocket_connection():
    """WebSocket 연결을 테스트합니다."""
    print(f"WebSocket URL: {websocket_url}")
    print("연결 테스트 시작...")
    
    try:
        # 연결 타임아웃을 10초로 설정
        websocket = await asyncio.wait_for(
            websockets.connect(websocket_url), 
            timeout=10.0
        )
        print("WebSocket 연결 성공!")
        
        # 연결 종료
        await websocket.close()
        print("연결 종료 완료")
        
    except asyncio.TimeoutError:
        print("연결 타임아웃 (10초)")
        print("가능한 원인:")
        print("   - 네트워크 연결 문제")
        print("   - 방화벽 차단")
        print("   - 서버 다운")
        
    except websockets.exceptions.InvalidURI:
        print("잘못된 WebSocket URL")
        print(f"   URL: {websocket_url}")
        
    except websockets.exceptions.ConnectionClosed:
        print("서버에서 연결을 거부했습니다")
        print("가능한 원인:")
        print("   - 인증 실패")
        print("   - 서버 정책 위반")
        
    except Exception as e:
        print(f"연결 실패: {e}")
        print("가능한 원인:")
        print("   - DNS 해결 실패")
        print("   - 네트워크 정책")
        print("   - 프록시 설정")

async def test_network_connectivity():
    """기본 네트워크 연결을 테스트합니다."""
    print("\n네트워크 연결 테스트...")
    
    import socket
    
    # 키움증권 서버 연결 테스트
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('mockapi.kiwoom.com', 10000))
        sock.close()
        
        if result == 0:
            print("키움증권 서버 포트 10000 연결 가능")
        else:
            print("키움증권 서버 포트 10000 연결 불가")
            print("방화벽이나 네트워크 정책을 확인하세요")
            
    except Exception as e:
        print(f"네트워크 테스트 실패: {e}")

if __name__ == "__main__":
    print("키움증권 WebSocket 연결 진단 도구")
    print("=" * 50)
    
    asyncio.run(test_network_connectivity())
    asyncio.run(test_websocket_connection())
    
    print("\n" + "=" * 50)
    print("해결 방법:")
    print("1. 방화벽에서 포트 10000 허용")
    print("2. 프록시 설정 확인")
    print("3. 네트워크 관리자에게 문의")
    print("4. 키움증권 서버 상태 확인")
