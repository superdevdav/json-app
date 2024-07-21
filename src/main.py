import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.models import create_tables
from rest.routes.engine.Engine_controller import router # Import generated controller

@asynccontextmanager
async def lifespan(app: FastAPI):
      await create_tables()
      print('INFO:     База данных создана')
      yield
      print('INFO:     Выключение')

app = FastAPI(lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
