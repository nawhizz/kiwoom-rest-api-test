#!/usr/bin/env python3
"""
다양한 import 방법 예제
"""

# 방법 1: setup_env.py를 먼저 실행한 후 사용
# python setup_env.py
# python example_import_methods.py

# 방법 2: 직접 sys.path 설정
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# 방법 3: 환경변수 PYTHONPATH 설정 후 사용
# Windows: set PYTHONPATH=%PYTHONPATH%;D:\Python_Test\kiwoom-rest-api
# Linux/Mac: export PYTHONPATH=$PYTHONPATH:/path/to/kiwoom-rest-api

def method1_direct_import():
    """방법 1: 직접 import (PYTHONPATH 설정 후)"""
    try:
        from chapter05.utils import KiwoomTR
        print("✅ 방법 1 성공: 직접 import")
        return True
    except ImportError as e:
        print(f"❌ 방법 1 실패: {e}")
        return False

def method2_relative_import():
    """방법 2: 상대 import"""
    try:
        from chapter05.utils import KiwoomTR
        print("✅ 방법 2 성공: 상대 import")
        return True
    except ImportError as e:
        print(f"❌ 방법 2 실패: {e}")
        return False

def method3_sys_path():
    """방법 3: sys.path 동적 추가"""
    import sys
    from pathlib import Path
    
    # 현재 파일의 부모 디렉토리를 sys.path에 추가
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    try:
        from chapter05.utils import KiwoomTR
        print("✅ 방법 3 성공: sys.path 동적 추가")
        return True
    except ImportError as e:
        print(f"❌ 방법 3 실패: {e}")
        return False

def method4_package_import():
    """방법 4: 패키지 import (__init__.py 사용)"""
    try:
        from chapter05 import KiwoomTR
        print("✅ 방법 4 성공: 패키지 import")
        return True
    except ImportError as e:
        print(f"❌ 방법 4 실패: {e}")
        return False

if __name__ == "__main__":
    print("=== 다양한 import 방법 테스트 ===\n")
    
    methods = [
        ("직접 import", method1_direct_import),
        ("상대 import", method2_relative_import),
        ("sys.path 동적 추가", method3_sys_path),
        ("패키지 import", method4_package_import),
    ]
    
    for name, method in methods:
        print(f"🔍 {name} 테스트:")
        method()
        print()
