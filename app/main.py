from fastapi import FastAPI
from app.routers.telemetry import router as telemetry_router

app = FastAPI()

app.include_router(telemetry_router)

@app.get("/")
async def hello_world():
    return {"message": "Hello World"}