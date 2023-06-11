# 2023 STEAM: 프로그래밍으로 문제 해결하기
> 과제 제출용 저장소입니다.

## Elasticsearch 세팅
해당 프로젝트는 한글 형태소 분석기로 *Nori*를 사용합니다.
```bash
elasticsearch-plugin install analysis-nori
```

## 백엔드(Python + Elasticsearch)

1. [여성가족부 누리집](http://www.mogef.go.kr/mp/pcd/mp_pcd_s001d.do?mid=plc502&bbtSn=704821)에서 .xlsx 파일을 다운로드합니다.
2. [전처리 스크립트](script/preprocess.py)를 실행합니다.

```bash
ELASTICSEARCH=<URL> ./script/preprocess.py PATH
# 또는
ELASTICSEARCH=<URL> python script/preprocess.py PATH
```

3. 명령어를 입력하여 실행 후 http://localhost:8000 으로 접속하여 확인합니다.

```bash
uvicorn src.main:app
```

## 프론트엔드(TypeScript + Vite)

### 개발 서버 실행

명령어를 입력하여 실행 후 http://localhost:5173 으로 접속하여 확인합니다.

```bash
yarn dev
```

### 빌드
```bash
yarn build
```

## 참고자료
[Elastic 가이드북](https://esbook.kimjmin.net/)