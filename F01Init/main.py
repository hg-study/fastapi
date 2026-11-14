# main.py — 최소 버전 (서버가 뜨는지 확인용)
from fastapi import FastAPI

app = FastAPI(title="ML API 첫걸음")

@app.get("/health")          # GET /health 주소를 만든다
def health():
    return {"status": "UP"}  # dict 를 return 하면 자동으로 JSON