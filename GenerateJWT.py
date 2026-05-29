#!/usr/bin/env python3
import sys
import time
import jwt
import os
from dotenv import load_dotenv  # 加这行

load_dotenv()  # 加这行 —— 加载 .env 文件

def get_token():
    # 从环境变量读取，而不是写死在代码里
    KEY_ID = os.getenv("HEWEATHER_KEY_ID", "")
    PROJECT_ID = os.getenv("HEWEATHER_PROJECT_ID", "")
    private_key = f"-----BEGIN PRIVATE KEY-----\n{os.getenv('HEWEATHER_PRIVATE_KEY', '')}\n-----END PRIVATE KEY-----"

    if not KEY_ID or not PROJECT_ID or not private_key:
        raise Exception("❌ 请先配置 .env 文件中的 API 信息！")

    payload = {
        'iat': int(time.time()) - 30,
        'exp': int(time.time()) + 86370,
        'sub': PROJECT_ID
    }
    headers = {
        'kid': KEY_ID
    }

    encoded_jwt = jwt.encode(payload, private_key, algorithm='EdDSA', headers=headers)
    return encoded_jwt
