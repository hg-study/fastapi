## FastAPI

### 목차

- [FastAPI Init](#fastapi-init)
- [FastAPI Basic](#fastapi-basic)
- [FastAPI CRUD](#fastapi-crud)
- [ML Fullstack Sample](#ml-fullstack-sample)

<br>

---

### FastAPI 시작과 자동 문서
- [FastAPI Init 이론](./Theory/01FastApiInit.md)
    - [F01Init main.py](./F01Init/main.py)
    - [Dockerfile](./F01Init/Dockerfile)
    - [compose 파일](./F01Init/docker-compose.yml)
    - [requirements](./F01Init/requirements.txt)

### 요청 본문, 파라미터, CORS
- [FastAPI Basic 이론](./Theory/02FastApiBasic.md)
    - [F02Basic main.py](./F02Basic/main.py)
    - [feature_spec.json](./F02Basic/feature_spec.json)
    - [Dockerfile](./F02Basic/Dockerfile)

### FastAPI로 CRUD 만들기
- [FastAPI CRUD 이론](./Theory/03FastApiCrud.md)
    - [MainBefore.py](./F03Crud/MainBefore.py)
    - [main.py](./F03Crud/main.py)
    - [store.py](./F03Crud/store.py)
    - [memos.db](./F03Crud/memos.db)

### ML 풀스택 샘플
- [ML Fullstack Sample 이론](./Theory/04MlFullstackSample.md)
    - [작업 지시서](./N01FireOccurrence/Docs/WorkOrder.html)
    - [단계별 상세 가이드](./N01FireOccurrence/S01Model/DetailGuide.html)
    - [모델 학습 노트북](./N01FireOccurrence/S01Model/ModelTraining.ipynb)
    - [데이터](./N01FireOccurrence/S01Model/data/FireOccurrenceSeoul.csv)
    - [타겟 분포](./N01FireOccurrence/Docs/Screens/01-1_TargetDistribution.png)
    - [ROC 곡선](./N01FireOccurrence/Docs/Screens/01-2_RocCurve.png)
    - [특성 중요도](./N01FireOccurrence/Docs/Screens/01-4_FeatureImportance.png)
    - [main.py](./N01FireOccurrence/S02FastApi/main.py)
    - [model.py](./N01FireOccurrence/S02FastApi/model.py)
    - [store.py](./N01FireOccurrence/S02FastApi/store.py)
    - [feature_spec.json](./N01FireOccurrence/S02FastApi/feature_spec.json)
    - [PredictionController](./N01FireOccurrence/S03Fullstack/Bn/src/main/java/com/example/demo/Controller/PredictionController.java)
    - [SecurityConfig](./N01FireOccurrence/S03Fullstack/Bn/src/main/java/com/example/demo/Config/SecurityConfig.java)
    - [application.properties](./N01FireOccurrence/S03Fullstack/Bn/src/main/resources/application.properties)
    - [Predict.jsx](./N01FireOccurrence/S03Fullstack/Fn/src/components/Predict.jsx)
    - [axiosConfig.js](./N01FireOccurrence/S03Fullstack/Fn/src/api/axiosConfig.js)
    - [실행 화면](./N01FireOccurrence/Docs/Screens/03-4_PredictFormAuto.png)
    - [compose 파일](./N01FireOccurrence/S03Fullstack/docker-compose.yml)
    - [DB Dockerfile](./N01FireOccurrence/S03Fullstack/DB/Dockerfile)
    - [FN Dockerfile](./N01FireOccurrence/S03Fullstack/Fn/Dockerfile)
    - [N02 모델 학습](./N02CropHeavyMetal/S01Model/ModelTraining.ipynb)
    - [N03 모델 학습](./N03BoatInspection/S01Model/ModelTraining.ipynb)
