# FastAPI Basic

- [요청 본문과 pydantic](#요청-본문과-pydantic)
- [경로 파라미터와 쿼리 파라미터](#경로-파라미터와-쿼리-파라미터)
- [CORS](#cors)
- [입력 항목 정의 파일](#입력-항목-정의-파일)

<br>

---

### 요청 본문과 pydantic

> POST 요청의 본문(body)은 `BaseModel`을 상속한 클래스로 모양을 선언한다. 함수 매개변수에 그 클래스를 쓰면 FastAPI가 JSON을 읽어 객체로 바꾸고, 타입이 맞지 않으면 자동으로 422 오류를 돌려준다. 같은 선언이 문서에도 반영된다. 입력 항목이 모델마다 다르므로 `Dict[str, Any]` 형태의 `features`로 받는다.

<br>

```python
class PredictRequest(BaseModel):
    features: Dict[str, Any]   # {"gu": 3, "month": 6}

@app.post("/predict")
def do_predict(req: PredictRequest):
    return {"받은_features": req.features}
```

<br>

- 예제 코드: [F02Basic main.py](../F02Basic/main.py)

---

### 경로 파라미터와 쿼리 파라미터

> 주소의 일부를 변수로 받는 것이 경로 파라미터이고, 주소 뒤 `?이름=값`으로 받는 것이 쿼리 파라미터이다. 경로 파라미터는 `{pid}`처럼 주소에 적고 같은 이름의 매개변수로 받는다. 함수에 있으나 주소에 없는 매개변수는 쿼리 파라미터가 되며 기본값을 주면 선택 항목이 된다. 타입 힌트(`int`)를 쓰면 문자열이 자동으로 정수로 변환된다.

<br>

| 구분 | 주소 예 | 함수 |
| --- | --- | --- |
| 경로 파라미터 | `/predictions/3` | `get_one(pid: int)` |
| 쿼리 파라미터 | `/predictions?limit=10` | `list_all(limit: int = 50)` |

---

### CORS

> 브라우저는 다른 출처(주소, 포트)로의 요청을 기본으로 막는다. React(3000 포트)가 FastAPI(8001 포트)나 Spring Boot를 직접 호출하려면 서버가 허용 출처를 응답 헤더로 알려 줘야 하며, FastAPI는 `CORSMiddleware`로 설정한다. 실습에서는 모든 출처를 허용(`*`)하지만 실제 서비스에서는 필요한 출처만 적는다.

<br>

```python
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])
```

---

### 입력 항목 정의 파일

> 예측 화면의 입력 폼을 코드에 고정하지 않고, `feature_spec.json`에 항목의 이름, 라벨, 형식(선택지, 숫자 범위)을 적어 두고 `/spec`으로 내려 준다. 프런트가 이 정의로 폼을 자동 생성하므로 모델이 바뀌어도 프런트 코드를 고치지 않아도 된다. `/health`는 서버 상태와 모델 이름을 반환해 Spring Boot의 헬스체크에 쓴다.

<br>

- 예제 코드: [feature_spec.json](../F02Basic/feature_spec.json), [Dockerfile](../F02Basic/Dockerfile)
