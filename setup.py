#!/usr/bin/env python3
"""
키움 REST API 패키지 설치 스크립트
"""

from setuptools import setup, find_packages

setup(
    name="kiwoom-rest-api",
    version="1.0.0",
    description="키움증권 REST API 및 WebSocket 예제 패키지",
    author="nawhizz",
    author_email="nawhizz@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.5",
        "pandas>=2.0.0",
        "websockets>=11.0.0",
        "loguru>=0.7.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
