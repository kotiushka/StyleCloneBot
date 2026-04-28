from fastapi import FastAPI
from src.api.routes import router
from src.db.database import engine

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup():
    pass 

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()