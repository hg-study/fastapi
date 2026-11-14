# FastAPI Init

- [FastAPI란](#fastapi란)
- [최소 서버](#최소-서버)
- [Docker 실행](#docker-실행)
- [자동 문서](#자동-문서)

<br>

---

### FastAPI란

> FastAPI는 파이썬 타입 힌트를 바탕으로 REST API를 빠르게 만드는 웹 프레임워크이다. 함수의 매개변수 타입으로 요청을 자동 검증하고, 반환한 딕셔너리를 JSON으로 바꾸며, 같은 정보로 API 문서(Swagger UI)까지 자동 생성한다. 이 저장소에서는 학습한 머신러닝 모델을 API로 감싸 Spring Boot와 React에서 호출하는 구조를 만든다.

<br>

```
React(FN) -> Spring Boot(BN) -> FastAPI(ML) -> model.pkl
```

<br>

| 요소 | 역할 |
| --- | --- |
| FastAPI | 모델을 서빙하고 예측 이력을 저장 |
| uvicorn | FastAPI를 실행하는 ASGI 서버 |
| pydantic | 요청 본문의 모양을 선언하고 검증 |

---

### 최소 서버

> `FastAPI()` 객체를 만들고 `@app.get("/health")` 같은 데코레이터로 주소와 함수를 연결한다. 딕셔너리를 반환하면 자동으로 JSON 응답이 된다. 서버가 뜨는지 확인하는 헬스체크 주소를 먼저 만들어 두면 이후 컨테이너 상태 확인과 연동 점검에 쓸 수 있다.

<br>

```python
from fastapi import FastAPI

app = FastAPI(title="ML API 첫걸음")

@app.get("/health")
def health():
    return {"status": "UP"}
```

<br>

- 예제 코드: [F01Init main.py](../F01Init/main.py)

---

### Docker 실행

> 파이썬 이미지에 `requirements.txt`의 라이브러리를 설치하고 `uvicorn main:app`으로 서버를 띄운다. `--host 0.0.0.0`은 컨테이너 밖에서 접속하도록 모든 인터페이스를 여는 설정이다. 개발 중에는 내 폴더를 컨테이너의 `/app`에 연결해 코드를 고치면 바로 반영되게 한다. `requirements.txt`에는 한글 주석을 넣지 않는다(pip가 읽다 깨진다).

<br>

| 파일 | 내용 |
| --- | --- |
| Dockerfile | `python:3.11-slim` 기반, 라이브러리 설치, 8001 포트 노출 |
| docker-compose.yml | 이미지 빌드, `8001:8001` 포트 연결, 폴더 볼륨, 자동 재시작 |
| requirements.txt | fastapi, uvicorn 등 버전 고정 |

<br>

```bash
docker compose up --build
```

<br>

- 예제 코드: [Dockerfile](../F01Init/Dockerfile), [compose 파일](../F01Init/docker-compose.yml), [requirements](../F01Init/requirements.txt)

---

### 자동 문서

> 서버를 실행하면 `/docs`에서 Swagger UI, `/redoc`에서 ReDoc 문서가 자동으로 만들어진다. 브라우저에서 각 엔드포인트의 요청 형식을 확인하고 바로 호출해 볼 수 있다. 예를 들어 `http://localhost:8001/docs`로 접속한다.
