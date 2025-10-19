#!/usr/bin/env python3
"""
환경 설정 스크립트
이 스크립트를 실행하면 PYTHONPATH가 자동으로 설정됩니다.
"""

import os
import sys
from pathlib import Path

def setup_pythonpath():
    """PYTHONPATH를 설정하여 프로젝트 루트를 추가합니다."""
    # 현재 스크립트의 디렉토리 (kiwoom-rest-api)
    current_dir = Path(__file__).parent.absolute()
    
    # 프로젝트 루트 디렉토리를 PYTHONPATH에 추가
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
        print(f"PYTHONPATH에 추가됨: {current_dir}")
    
    return current_dir

if __name__ == "__main__":
    setup_pythonpath()
    print("환경 설정 완료!")
    print("이제 다음과 같이 import할 수 있습니다:")
    print("from chapter05.utils import KiwoomTR")
