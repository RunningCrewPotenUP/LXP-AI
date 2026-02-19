import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.ai.models import SentenceEmbedder

class ProductService:
    def __init__(self, db: AsyncSession, embedder: SentenceEmbedder):
        self.db = db
        self.embedder = embedder

    async def create_product(self, product_data):
        combined_text = f"{product_data.name} {product_data.description}"
        vector = await asyncio.to_thread(self.embedder.get_embedding, combined_text)
        
        new_product = Product(**product_data.dict(), embedding=vector)
        self.db.add(new_product)
        await self.db.commit()
        return new_product