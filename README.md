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
CREATE TABLE public.lectures (
	id serial4 NOT NULL,
	lecture_id int8 NOT NULL,
	course_title varchar(255) NOT NULL,
	course_description varchar(255) NULL,
	section_title varchar(255) NOT NULL,
	lecture_title varchar(255) NOT NULL,
	"difficulty" public."difficulty" NULL,
	script_content text NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT lectures_pkey PRIMARY KEY (id)
);

CREATE TABLE public.products (
	id serial4 NOT NULL,
	"name" varchar(255) NOT NULL,
	brand varchar(100) NULL,
	price int4 NOT NULL,
	image_url text NULL,
	purchase_url text NULL,
	description text NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT products_pkey PRIMARY KEY (id)
);

CREATE TABLE public.baai_lecture (
	id serial4 NOT NULL,
	lecture_id int4 NOT NULL,
	vector public.vector NULL,
  summary_content text NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT baai_lecture_pkey PRIMARY KEY (id),
	CONSTRAINT fk_lecture FOREIGN KEY (lecture_id) REFERENCES public.lectures(id) ON DELETE CASCADE
);
CREATE INDEX idx_baai_lecture_vector ON public.baai_lecture USING hnsw (vector vector_cosine_ops);

CREATE TABLE public.baai_product (
	id serial4 NOT NULL,
	product_id int4 NOT NULL,
	vector public.vector NULL,
  summary_content text NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT baai_product_pkey PRIMARY KEY (id),
	CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE
);
CREATE INDEX idx_baai_product_vector ON public.baai_product USING hnsw (vector vector_cosine_ops);

CREATE TABLE public.dragonkue_baai_lecture (
	id serial4 NOT NULL,
	lecture_id int4 NOT NULL,
	vector public.vector NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT dragonkue_baai_lecture_pkey PRIMARY KEY (id),
	CONSTRAINT fk_lecture FOREIGN KEY (lecture_id) REFERENCES public.lectures(id) ON DELETE CASCADE
);

CREATE TABLE public.dragonkue_baai_product (
	id serial4 NOT NULL,
	product_id int4 NOT NULL,
	vector public.vector NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT dragonkue_baai_product_pkey PRIMARY KEY (id),
	CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE
);
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