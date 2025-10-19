#!/usr/bin/env python3
"""
__init__.py를 사용한 패키지 import 예제

이 파일은 __init__.py를 통해 설정된 패키지 구조를 사용하는 방법을 보여줍니다.
"""

def example1_package_level_import():
    """방법 1: 패키지 레벨에서 직접 import"""
    print("=== 방법 1: 패키지 레벨 import ===")
    try:
        # 프로젝트 루트에서 KiwoomTR을 직접 import
        from kiwoom_rest_api import KiwoomTR
        
        # KiwoomTR 인스턴스 생성
        kiwoom = KiwoomTR()
        print("✅ 패키지 레벨 import 성공!")
        print(f"토큰: {kiwoom.token[:20]}...")
        return True
    except ImportError as e:
        print(f"❌ Import 실패: {e}")
        return False

def example2_chapter_level_import():
    """방법 2: 챕터 레벨에서 import"""
    print("\n=== 방법 2: 챕터 레벨 import ===")
    try:
        # chapter05에서 KiwoomTR import
        from chapter05 import KiwoomTR
        
        # KiwoomTR 인스턴스 생성
        kiwoom = KiwoomTR()
        print("✅ 챕터 레벨 import 성공!")
        print(f"토큰: {kiwoom.token[:20]}...")
        return True
    except ImportError as e:
        print(f"❌ Import 실패: {e}")
        return False

def example3_websocket_import():
    """방법 3: WebSocket 클래스 import"""
    print("\n=== 방법 3: WebSocket 클래스 import ===")
    try:
        # chapter06에서 WebSocketClient import
        from chapter06 import WebSocketClient
        from chapter06.config import websocket_url
        
        print("✅ WebSocket 클래스 import 성공!")
        print(f"WebSocket URL: {websocket_url}")
        return True
    except ImportError as e:
        print(f"❌ Import 실패: {e}")
        return False

def example4_multiple_imports():
    """방법 4: 여러 클래스 동시 import"""
    print("\n=== 방법 4: 여러 클래스 동시 import ===")
    try:
        # 여러 패키지에서 동시에 import
        from chapter05 import KiwoomTR, log_exceptions
        from chapter06 import WebSocketClient
        
        print("✅ 여러 클래스 동시 import 성공!")
        print(f"KiwoomTR: {KiwoomTR}")
        print(f"log_exceptions: {log_exceptions}")
        print(f"WebSocketClient: {WebSocketClient}")
        return True
    except ImportError as e:
        print(f"❌ Import 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 __init__.py를 사용한 패키지 import 테스트\n")
    
    # 프로젝트 루트를 sys.path에 추가
    import sys
    from pathlib import Path
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"📁 프로젝트 루트 추가: {project_root}\n")
    
    # 각 방법 테스트
    methods = [
        example1_package_level_import,
        example2_chapter_level_import,
        example3_websocket_import,
        example4_multiple_imports,
    ]
    
    success_count = 0
    for method in methods:
        if method():
            success_count += 1
    
    print(f"\n📊 결과: {success_count}/{len(methods)} 방법 성공")
    
    if success_count == len(methods):
        print("🎉 모든 import 방법이 성공했습니다!")
        print("\n💡 이제 다음과 같이 사용할 수 있습니다:")
        print("   from kiwoom_rest_api import KiwoomTR")
        print("   from chapter05 import KiwoomTR")
        print("   from chapter06 import WebSocketClient")
    else:
        print("⚠️  일부 import가 실패했습니다. 환경 설정을 확인해주세요.")

if __name__ == "__main__":
    main()
