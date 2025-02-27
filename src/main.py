import uvicorn
from fastapi import FastAPI

from src.core.logging import setup_logging
from .api.v1 import router as v1_router

setup_logging()

app = FastAPI()

app.include_router(v1_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
