from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import store
store.init_db()          # ← 앱 시작 시 테이블 준비 (한 번)

app = FastAPI()

class Memo(BaseModel):
    text: str

@app.post("/memos", status_code=201)      # C : 생성
def create_memo(m: Memo):
    return store.create(m.text)

@app.get("/memos")                        # R : 목록
def list_memos():
    return store.list_all()

@app.get("/memos/{mid}")                  # R : 단건
def get_memo(mid: int):
    row = store.get(mid)
    if row is None:
        raise HTTPException(404, "그런 메모 없음")
    return row


@app.put("/memos/{mid}")                  # U : 수정
def update_memo(mid: int, m: Memo):
    row = store.update(mid, m.text)
    if row is None:
        raise HTTPException(404, "그런 메모 없음")
    return row

@app.delete("/memos/{mid}")               # D : 삭제
def delete_memo(mid: int):
    if not store.delete(mid):
        raise HTTPException(404, "그런 메모 없음")
    return {"deleted": mid}