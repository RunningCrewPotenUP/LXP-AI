# 강의 기반 상품 추천 서비스
- 강의와 상품의 연관도를 비교하여 상품을 추천하는 서비스

### 로컬 실행
```bash
uv run uvicorn app.main:app --reload
```

### 데이터베이스 설정
- PostgreSQL의 pgvector 기능을 활성화 하여 사용
- 도커 환경에서 PostgreSQL의 이미지에는 pgvector를 포함하지 않으므로 pgvector 이미지를 사용

```yml
services:
  postgres:
    image: pgvector/pgvector:pg15
    restart: always
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    ports:
      - "15432:5432"
    environment:
      POSTGRES_USER: running-crew
      POSTGRES_PASSWORD: running-crew
      POSTGRES_DB: running-crew
```

- Schema
``` sql
CREATE EXTENSION IF NOT EXISTS vector;
SELECT * FROM pg_extension; -- vector 사용 가능 여부 확인

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(id),
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(100),
    price INT NOT NULL,
    image_url TEXT,
    purchase_url TEXT,
    description TEXT,
    embedding VECTOR(1024),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE difficulty AS ENUM('EXPERT','JUNIOR','MIDDLE','SENIOR');

CREATE TABLE lectures (
    id SERIAL PRIMARY KEY,
    lecture_id BIGINT NOT NULL,
    course_title VARCHAR(255) NOT NULL,
    course_description VARCHAR(255),
    section_title VARCHAR(255) NOT NULL,
    lecture_title VARCHAR(255) NOT NULL,
    difficulty difficulty,
    script_content TEXT,
    embedding VECTOR(1024),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ON products USING hnsw (embedding vector_cosine_ops);
```

- PostgreSQL 벡터 비교 예시
```sql
SELECT 
    p.name, 
    p.price, 
    p.image_url, 
    p.purchase_url,
    1 - (p.embedding <=> l.embedding) AS similarity_score
FROM products p, lectures l
WHERE l.id = 10
ORDER BY similarity_score DESC
LIMIT 5;
```

### ORM - SQLAlchemy
- 파이썬 생태계에서 가장 오래 사용되고 검증된 `SQLAlchemy`를 사용
- SQLModel

##### 필요한 라이브러리 설정
```bash
uv add sqlalchemy asyncpg python-dotenv pydantic-settings pgvector
```
- PostgreSQL의 VECTOR 타입을 SQLAlchemy 모델을 사용하려면 pgvector 라이브러리 필요