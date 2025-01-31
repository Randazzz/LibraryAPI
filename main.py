from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.database import get_db

app = FastAPI()


@app.get("/",)
async def get_user():
    user = {
        "username": "testuser",
        "password": "testpassword",
    }
    return user


@app.get("/test-db")
async def db_connection(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(1))
    return {"status": "success", "result": result.scalars().all()}

