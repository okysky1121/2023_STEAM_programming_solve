# 2023 STEAM: 프로그래밍으로 문제 해결하기
과제 제출용 저장소입니다.

## 1. 엑셀 파일 가져오기
[여성가족부 누리집](http://www.mogef.go.kr/mp/pcd/mp_pcd_s001d.do?mid=plc502&bbtSn=704821)에서 .xlsx 파일을 다운로드합니다.

## 2. 데이터 전처리 작업하기
위의 파일에서 필요한 정보만을 가져와 fetch_data.csv 파일을 생성합니다.

### Windows
```bat
python script\preprocess.py PATH
```

### Linux
```bash
./script/preprocess.py PATH
```

## 3. 서버 실행하기
```bash
uvicorn src.main:app --port PORT
```
위의 명령어를 입력하여 실행 후 http://localhost:PORT 로 접속하여 테스트합니다.