# ML Fullstack Sample

- [전체 구조](#전체-구조)
- [모델 학습 노트북](#모델-학습-노트북)
- [ML API 서버](#ml-api-서버)
- [Spring Boot 중계](#spring-boot-중계)
- [React 화면](#react-화면)
- [Docker Compose 통합](#docker-compose-통합)
- [세 가지 샘플](#세-가지-샘플)

<br>

---

### 전체 구조

> 공공데이터로 이진 분류 모델을 학습하고, FastAPI로 서빙하고, Spring Boot와 React로 화면까지 붙이는 과정을 세 단계로 나눈 완성 샘플이다. 한 샘플은 `S01Model`(학습), `S02FastApi`(ML API), `S03Fullstack`(통합)과 실행 화면 캡처, 작업 지시서로 구성된다.

<br>

| 단계 | 폴더 | 내용 |
| --- | --- | --- |
| 1 | S01Model | 데이터 분석, 모델 학습, `model.pkl`과 `feature_spec.json` 저장 |
| 2 | S02FastApi | 모델 서빙, 예측 이력 CRUD(SQLite) |
| 3 | S03Fullstack | Spring Boot(Bn), React(Fn), MySQL, Redis, compose |

<br>

- 예제 코드: [작업 지시서](../N01FireOccurrence/Docs/WorkOrder.html), [단계별 상세 가이드](../N01FireOccurrence/S01Model/DetailGuide.html)

---

### 모델 학습 노트북

> 표준 흐름은 로드, EDA, 결측치 처리, 타겟 분리와 인코딩, 분할(stratify), 학습, 평가(ROC-AUC), 저장의 8단계이다. 이 샘플의 핵심은 불균형 데이터 다루기와 데이터 누수 방지이다.

<br>

| 주제 | 내용 |
| --- | --- |
| 불균형 | 인명피해 없는 화재가 약 96%여서 정확도만 보면 속는다. 정확도 대신 ROC-AUC를 함께 보고, `class_weight='balanced'`로 소수 클래스를 더 중요하게 학습한다. 옵션을 빼면 정확도는 높지만 실제 피해 화재를 거의 놓친다. |
| 누수 방지 | 사망, 부상, 인명피해 소계는 타겟 자체이므로 입력에서 뺀다. 결측치를 채울 때도 전체가 아니라 학습 데이터 기준으로 채운다. |
| 분할 | `stratify=y`로 학습, 검증의 클래스 비율을 같게 유지 |
| 과적합 억제 | 랜덤 포레스트 `max_depth=8`로 깊이 제한, 파일 크기도 줄임 |
| 해석 | 특성 중요도로 데이터에서 읽은 인사이트(발화요인 등)를 모델도 배웠는지 대조 |
| 저장 | `joblib`으로 `model.pkl` 저장, 입력 정의는 `feature_spec.json` |

<br>

- 예제 코드: [모델 학습 노트북](../N01FireOccurrence/S01Model/ModelTraining.ipynb), [데이터](../N01FireOccurrence/S01Model/data/FireOccurrenceSeoul.csv), [타겟 분포](../N01FireOccurrence/Docs/Screens/01-1_TargetDistribution.png), [ROC 곡선](../N01FireOccurrence/Docs/Screens/01-2_RocCurve.png), [특성 중요도](../N01FireOccurrence/Docs/Screens/01-4_FeatureImportance.png)

---

### ML API 서버

> 앱이 시작될 때 모델과 입력 정의를 한 번만 읽어 메모리에 두고(캐싱) 요청마다 재사용한다. 예측 로직은 `run_model` 한 곳에 모아 예측만 하는 엔드포인트와 CRUD 엔드포인트가 함께 쓴다. 이력은 SQLite(`store.py`)에 저장하고 없는 번호는 404로 응답한다. 예측 입력은 `DataFrame` 한 행으로 만들어 `predict`와 `predict_proba`를 호출한다.

<br>

| 엔드포인트 | 역할 |
| --- | --- |
| `GET /health` | 서버와 모델 상태 |
| `GET /spec` | 입력 항목 정의(폼 자동 생성용) |
| `POST /predict` | 예측만 수행, 저장 안 함 |
| `POST /predictions` | 예측 후 이력 저장(C) |
| `GET /predictions`, `/predictions/{id}` | 이력 조회(R) |
| `PUT /predictions/{id}` | 입력을 바꿔 다시 예측하고 갱신(U) |
| `DELETE /predictions/{id}` | 이력 삭제(D) |

<br>

- 예제 코드: [main.py](../N01FireOccurrence/S02FastApi/main.py), [model.py](../N01FireOccurrence/S02FastApi/model.py), [store.py](../N01FireOccurrence/S02FastApi/store.py), [feature_spec.json](../N01FireOccurrence/S02FastApi/feature_spec.json)

---

### Spring Boot 중계

> Spring Boot는 모델을 직접 다루지 않고 인증과 중계만 맡는다. `/api/predict`, `/api/predictions` 요청을 받아 `RestTemplate`으로 FastAPI에 그대로 전달하고 응답을 돌려준다. FastAPI 주소는 `ml.url` 설정으로 주입한다. 회원가입과 로그인은 JWT와 Redis 기반 인증(OAuth2 소셜 로그인 포함)으로 처리하고, 로그인하지 않으면 예측 API를 쓸 수 없다. 사용자 정보는 MySQL에 저장한다. 인증 구조 자체는 Spring Boot 저장소의 시큐리티 이론을 따른다.

<br>

| 구성 | 역할 |
| --- | --- |
| PredictionController | FastAPI 예측 API 중계 |
| UserRestController | 회원가입, 로그인 |
| SecurityConfig | 경로별 접근 권한 |
| JWT 패키지 | 토큰 발급, 검증 필터 |
| Redis 패키지 | 토큰 저장소 |

<br>

- 예제 코드: [PredictionController](../N01FireOccurrence/S03Fullstack/Bn/src/main/java/com/example/demo/Controller/PredictionController.java), [SecurityConfig](../N01FireOccurrence/S03Fullstack/Bn/src/main/java/com/example/demo/Config/SecurityConfig.java), [application.properties](../N01FireOccurrence/S03Fullstack/Bn/src/main/resources/application.properties)

---

### React 화면

> 화면은 `/api/spec`으로 받은 입력 정의를 보고 폼을 자동으로 그린다. 선택지가 있는 항목은 선택 상자, 숫자 항목은 범위가 있는 입력으로 만든다. 예측 결과(라벨과 확률)를 보여 주고 이력을 표로 나열하며, 이력의 수정 모드와 삭제를 제공한다. axios의 `withCredentials` 설정으로 로그인 쿠키(토큰)가 요청마다 함께 전송된다.

<br>

- 예제 코드: [Predict.jsx](../N01FireOccurrence/S03Fullstack/Fn/src/components/Predict.jsx), [axiosConfig.js](../N01FireOccurrence/S03Fullstack/Fn/src/api/axiosConfig.js), [실행 화면](../N01FireOccurrence/Docs/Screens/03-4_PredictFormAuto.png)

---

### Docker Compose 통합

> 데이터베이스(db), 캐시(redis), ML API(ml), 프런트(fn), 백엔드(bn) 다섯 컨테이너를 compose 하나로 묶는다. 각 컨테이너에 고정 IP를 주고 서로를 컨테이너 이름으로 부른다. Spring Boot는 `db-container`, `redis-container`, `ml-container`라는 이름으로 접근하므로 설정의 호스트도 그 이름을 쓴다.

<br>

| 컨테이너 | 호스트 포트 | 내용 |
| --- | --- | --- |
| db | 3330 | MySQL |
| redis | 6380 | Redis |
| ml | 8001 | FastAPI |
| fn | 3000 | React를 nginx로 서비스 |
| bn | 8080 | Spring Boot |

<br>

- 예제 코드: [compose 파일](../N01FireOccurrence/S03Fullstack/docker-compose.yml), [DB Dockerfile](../N01FireOccurrence/S03Fullstack/DB/Dockerfile), [FN Dockerfile](../N01FireOccurrence/S03Fullstack/Fn/Dockerfile)

---

### 세 가지 샘플

> 세 샘플은 같은 구조에 데이터만 바꾼 것이다. 입력 정의와 모델이 다르고 나머지 코드의 뼈대는 같다.

<br>

| 폴더 | 주제 | 데이터 |
| --- | --- | --- |
| N01FireOccurrence | 서울 화재 인명피해 예측 | FireOccurrenceSeoul.csv |
| N02CropHeavyMetal | 농산물 중금속 분석 결과 예측 | CropHeavyMetalResult.csv |
| N03BoatInspection | 어선 검사 현황 예측 | BoatInspectionStatus.csv |

<br>

- 예제 코드: [N02 모델 학습](../N02CropHeavyMetal/S01Model/ModelTraining.ipynb), [N03 모델 학습](../N03BoatInspection/S01Model/ModelTraining.ipynb)
