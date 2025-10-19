#!/usr/bin/env python3
"""
chapter06 실행 스크립트
환경 설정을 자동으로 수행한 후 example6-1.py를 실행합니다.
"""

import sys
from pathlib import Path

def setup_environment():
    """실행 환경을 설정합니다."""
    # 프로젝트 루트 디렉토리를 sys.path에 추가
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"✅ 환경 설정 완료: {project_root}")

def main():
    """메인 실행 함수"""
    print("🚀 키움 REST API Chapter06 실행 중...")
    
    # 환경 설정
    setup_environment()
    
    try:
        # chapter06의 example6_1.py 실행
        from chapter06.example6_1 import main as chapter06_main
        chapter06_main()
    except ImportError as e:
        print(f"❌ Import 오류: {e}")
        print("💡 해결 방법:")
        print("   1. setup_env.py를 먼저 실행하세요")
        print("   2. 또는 PYTHONPATH 환경변수를 설정하세요")
        print("   3. 또는 pip install -e . 로 패키지를 설치하세요")
    except Exception as e:
        print(f"❌ 실행 오류: {e}")

if __name__ == "__main__":
    main()
