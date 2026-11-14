from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
memos = []          # 메모리 저장소 (리스트) — 서버 끄면 사라짐!
next_id = 1

class Memo(BaseModel):
    text: str

@app.post("/memos", status_code=201)      # C : 생성
def create_memo(m: Memo):
    global next_id
    row = {"id": next_id, "text": m.text}
    memos.append(row); next_id += 1
    return row

@app.get("/memos")                        # R : 목록
def list_memos():
    return memos

@app.get("/memos/{mid}")                  # R : 단건
def get_memo(mid: int):
    for row in memos:
        if row["id"] == mid:
            return row
    raise HTTPException(404, "그런 메모 없음")

@app.put("/memos/{mid}")                  # U : 수정
def update_memo(mid: int, m: Memo):
    for row in memos:
        if row["id"] == mid:
            row["text"] = m.text
            return row
    raise HTTPException(404, "그런 메모 없음")

@app.delete("/memos/{mid}")               # D : 삭제
def delete_memo(mid: int):
    global memos
    before = len(memos)
    memos = [r for r in memos if r["id"] != mid]
    if len(memos) == before:
        raise HTTPException(404, "그런 메모 없음")
    return {"deleted": mid}