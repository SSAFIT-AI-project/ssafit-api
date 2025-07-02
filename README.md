<div align="center">
  <img src="https://via.placeholder.com/400x200/4F46E5/FFFFFF?text=SSAFIT+API" alt="SSAFIT API Logo" width="400"/>
  <h1>SSAFIT API - 신용카드 추천 및 AI 상담 서비스</h1>
</div>

## 📋 프로젝트 소개

SSAFIT API는 신용카드 정보를 제공하고 AI 상담 서비스를 제공하는 FastAPI 기반 웹 애플리케이션입니다.

### 주요 기능
- **카드 정보 조회**: 다양한 신용카드의 상세 정보 제공
- **인기 카드 추천**: 사용자 인기도 기반 카드 추천
- **AI 상담 서비스**: RAG(Retrieval-Augmented Generation) 기반의 지능형 카드 상담
- **벡터 검색**: Chroma DB를 활용한 효율적인 문서 검색

### 기술 스택
- **Backend**: FastAPI (Python)
- **AI/ML**: LangChain, Upstage LLM (Solar-1-mini-chat)
- **Vector Database**: Chroma DB
- **Embedding**: Upstage Embeddings
- **Search**: MMR (Maximum Marginal Relevance) 검색

## 🚀 서버 실행 방법

### 1. 가상환경 설정
```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정
`.env` 파일을 생성하고 다음 내용을 추가하세요:
```env
UPSTAGE_API_KEY=your_upstage_api_key_here
```

### 3. ngrok 설정 (HTTPS 지원)
```bash
# ngrok 설치 (아직 설치되지 않은 경우)
# https://ngrok.com/download 에서 다운로드

# ngrok 실행 (새 터미널에서)
ngrok http 8000
```

### 4. 서버 실행
```bash
# 메인 서버 실행
python main.py
```

서버가 `http://0.0.0.0:8000`에서 실행됩니다.

## 📚 API 엔드포인트

### 기본 엔드포인트
- `GET /`: API 정보 및 사용 가능한 엔드포인트 목록
- `GET /docs`: Swagger UI 문서 (자동 생성)

### 카드 관련 엔드포인트
- `GET /cards`: 모든 카드 정보 조회
- `GET /popular-cards`: 인기 카드 정보 조회

### AI 상담 엔드포인트
- `POST /ask`: AI 카드 상담 서비스
  ```json
  {
    "question": "연회비가 없는 카드를 추천해주세요"
  }
  ```

## 🔧 프로젝트 구조

```
ssafit-api/
├── main.py                 # FastAPI 메인 애플리케이션
├── requirements.txt        # Python 패키지 의존성
├── .env.example           # 환경변수 예시 파일
├── .gitignore             # Git 무시 파일 목록
├── data/                  # 데이터 파일들
│   ├── cards_data.py      # 카드 데이터
│   └── popular_cards_data.py  # 인기 카드 데이터
├── routes/                # API 라우터
│   ├── cards.py          # 카드 관련 엔드포인트
│   └── ask.py            # AI 상담 엔드포인트
├── chroma_db/            # 벡터 데이터베이스 (자동 생성 또는 파일 수동 삽입)
└── venv/                 # 가상환경 (자동 생성)
```

## 🌐 접속 방법

### 로컬 접속
- API 문서: `http://localhost:8000/docs`
- 서버 상태: `http://localhost:8000/`

### 외부 접속 (ngrok 사용)
- API 문서: `https://[ngrok-url]/docs`
- 서버 상태: `https://[ngrok-url]/`

## 🔍 주요 특징

### RAG 시스템
- **Retrieval**: Chroma DB를 통한 벡터 검색
- **Generation**: Upstage Solar-1-mini-chat 모델을 통한 답변 생성
- **MMR 검색**: 유사성과 다양성을 모두 고려한 검색 결과

### 데이터 관리
- 카드 정보는 구조화된 JSON 형태로 관리
- 벡터 데이터베이스로 효율적인 검색 지원
- 메타데이터를 통한 정확한 카드 식별

## 📝 개발자 정보

- **프로젝트**: SSAFIT API
- **버전**: 1.0.0
- **라이선스**: MIT

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요. 