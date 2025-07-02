from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import cards, ask
import os

# 환경변수 로드 (강제로 현재 디렉토리에서 .env 파일 찾기)
load_dotenv(override=True)

# API 키 확인
api_key = os.getenv("UPSTAGE_API_KEY")
if api_key:
    print(f"API 키 로드됨: {api_key[:10]}...")
else:
    print("경고: UPSTAGE_API_KEY를 찾을 수 없습니다.")


# FastAPI 앱 생성
app = FastAPI(
    title="신용카드 추천 API",
    description="신용카드 정보 조회 및 AI 상담 서비스",
    version="1.0.0"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 라우터 등록
app.include_router(cards.router, tags=["cards"])
app.include_router(ask.router, tags=["ask"])

@app.get("/")
def read_root():
    """루트 엔드포인트"""
    return {
        "message": "신용카드 추천 API에 오신 것을 환영합니다!",
        "endpoints": {
            "cards": "/cards - 모든 카드 정보 조회",
            "ask": "/ask - AI 상담 서비스"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 