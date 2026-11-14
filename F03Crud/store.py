
#----------------------------
# SQLite 저장소
#----------------------------
import json
import sqlite3
from datetime import datetime

DB_PATH = "memos.db"        # DB 는 파일 하나로 생긴다

def _con():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row  # 결과를 dict 처럼 쓰기 위함
    return con

def init_db():
    """메모 테이블 생성 (앱 시작 시 1회)"""
    con = _con()
    try:
        con.execute("""
            CREATE TABLE IF NOT EXISTS memos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                text        TEXT NOT NULL,
                created_at  TEXT NOT NULL
            )
        """)
        con.commit()
    finally:
        con.close()


#----------------------------
# 응용 CRUD — 예측 이력
#----------------------------

def _to_dict(r):        # DB 한 줄 → 파이썬 dict (json 은 되돌림)
    return {"id": r["id"], "text": json.loads(r["text"]), "created_at": r["created_at"]}

def create(text):                     # C
    con = _con()
    try:
        cur = con.execute(
            "INSERT INTO memos(text, created_at) VALUES (?, ?)",
            (json.dumps(text, ensure_ascii=False), 
             datetime.now().isoformat(timespec="seconds")))
        con.commit(); pid = cur.lastrowid
    finally:
        con.close()
    return get(pid)

def get(pid):                                     # R : 단건 (없으면 None)
    con = _con()
    try:
        r = con.execute("SELECT * FROM memos WHERE id = ?", (pid,)).fetchone()
    finally:
        con.close()
    return _to_dict(r) if r else None

def list_all(limit=50):                           # R : 목록 (최신순)
    con = _con()
    try:
        rows = con.execute("SELECT * FROM memos ORDER BY id DESC LIMIT ?",
                           (limit,)).fetchall()
    finally:
        con.close()
    return [_to_dict(r) for r in rows]

def update(pid, text):                # U
    con = _con()
    try:
        cur = con.execute(
            "UPDATE memos SET text=? WHERE id=?",
            (json.dumps(text, ensure_ascii=False), pid))
        con.commit(); changed = cur.rowcount
    finally:
        con.close()
    return get(pid) if changed else None

def delete(pid):                                  # D (지운 게 있으면 True)
    con = _con()
    try:
        cur = con.execute("DELETE FROM memos WHERE id = ?", (pid,))
        con.commit(); return cur.rowcount > 0
    finally:
        con.close()