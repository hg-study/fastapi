# main.py — 최소 버전 (서버가 뜨는지 확인용)
import json
from fastapi import FastAPI

app = FastAPI(title="ML API 첫걸음")

# @app.get("/health")          # GET /health 주소를 만든다
# def health():
#     return {"status": "UP"}  # dict 를 return 하면 자동으로 JSON


# ------------------------------------------------------
# 02 기본기능
# ------------------------------------------------------
from pydantic import BaseModel
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware

# React/Spring Boot 에서 호출을 허용 (CORS)
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

# 입력 항목 정의를 파일에서 한 번 읽어둔다
spec = json.load(open("feature_spec.json", encoding="utf-8"))


# 요청 본문(body)의 모양을 미리 선언한다
class PredictRequest(BaseModel):
    features: Dict[str, Any]   # {"gu": 3, "month": 6, ...}

@app.post("/predict")
def do_predict(req: PredictRequest):   # ← 자동으로 검증 + 문서화
    return {"받은_features": req.features}

# 경로 파라미터: 주소의 일부를 변수로 받는다
@app.get("/predictions/{pid}")     # /predictions/3  →  pid = 3
def get_one(pid: int):
    return {"요청한_id": pid}

# 쿼리 파라미터: 주소 뒤 ?이름=값 으로 받는다 (기본값 지정 가능)
@app.get("/predictions")           # /predictions?limit=10  →  limit = 10
def list_all(limit: int = 50):     # 안 주면 50
    return {"최대개수": limit}

@app.get("/health")
def health():
    """서버가 살아있는지 확인 (BN 헬스체크용)"""
    return {"status": "UP", "model": spec["title"]}

@app.get("/spec")
def get_spec():
    """입력 항목 정의(라벨·선택지) - FN 폼 자동 생성에 사용"""
    return spec