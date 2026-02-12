from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_size=10,  # 기본 연결 풀 크기
    max_overflow=20,  # 최대 추가 연결 수
    pool_timeout=30,  # 연결 대기 타임아웃 (초)
    pool_recycle=3600,  # 연결 재활용 주기 (1시간)
    pool_pre_ping=True  # 연결 사용 전 핑 테스트
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session