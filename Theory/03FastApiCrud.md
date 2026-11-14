# FastAPI CRUD

- [CRUD와 HTTP 메서드](#crud와-http-메서드)
- [메모리 저장소](#메모리-저장소)
- [SQLite 저장소](#sqlite-저장소)
- [오류 응답](#오류-응답)

<br>

---

### CRUD와 HTTP 메서드

> CRUD는 데이터의 생성(Create), 조회(Read), 수정(Update), 삭제(Delete)이며 REST API에서는 각각 POST, GET, PUT, DELETE에 대응한다. 생성은 성공 상태 코드를 `201`로 지정한다.

<br>

| 동작 | 메서드 | 주소 | 상태 코드 |
| --- | --- | --- | --- |
| 생성 | POST | `/memos` | 201 |
| 목록 | GET | `/memos` | 200 |
| 단건 | GET | `/memos/{mid}` | 200, 없으면 404 |
| 수정 | PUT | `/memos/{mid}` | 200, 없으면 404 |
| 삭제 | DELETE | `/memos/{mid}` | 200, 없으면 404 |

---

### 메모리 저장소

> 처음에는 파이썬 리스트에 저장해 CRUD 흐름만 익힌다. 구현이 가장 단순하지만 서버를 끄면 데이터가 사라진다. 번호는 전역 변수 `next_id`를 올려 가며 붙이고, 삭제는 해당 번호를 뺀 리스트를 새로 만들어 대입한다(전역 변수를 바꾸므로 `global` 선언이 필요하다).

<br>

- 예제 코드: [MainBefore.py](../F03Crud/MainBefore.py)

---

### SQLite 저장소

> 데이터를 파일에 보관하려고 파이썬 내장 `sqlite3`로 저장소 모듈(`store.py`)을 분리한다. DB는 파일 하나(`memos.db`)로 생기고, 앱이 시작될 때 `CREATE TABLE IF NOT EXISTS`로 테이블을 준비한다. `row_factory = sqlite3.Row`로 결과를 딕셔너리처럼 쓰고, 값은 `?` 자리표시자로 넘겨 SQL 인젝션을 막는다. 연결은 `try / finally`로 반드시 닫는다. 객체 형태의 값은 `json.dumps`로 문자열로 저장하고 읽을 때 `json.loads`로 되돌린다.

<br>

| 함수 | 역할 |
| --- | --- |
| `init_db()` | 테이블 준비 |
| `create(text)` | 추가 후 새 행 반환 |
| `get(pid)` | 단건, 없으면 None |
| `list_all(limit)` | 최신순 목록 |
| `update(pid, text)` | 수정, 없으면 None |
| `delete(pid)` | 삭제, 지운 행이 있으면 True |

<br>

- 예제 코드: [main.py](../F03Crud/main.py), [store.py](../F03Crud/store.py), [memos.db](../F03Crud/memos.db)

---

### 오류 응답

> 대상이 없을 때는 `raise HTTPException(404, "메시지")`로 상태 코드와 메시지를 돌려준다. 조회한 결과가 `None`인지 확인한 뒤 던져야 하며, `return` 뒤에 `raise`를 두면 실행되지 않는다. 메시지는 `{"detail": "..."}` 형태의 JSON으로 응답된다.
