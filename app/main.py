from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.telemetry import router as telemetry_router
from app.routers.drivers import router as drivers_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(telemetry_router)
app.include_router(drivers_router)

@app.get("/")
async def hello_world():
    return {"message": "Hello World"}