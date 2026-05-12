from fastapi import APIRouter
from app.services.telemetry import get_driver_laps, get_tyre_degradation

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

@router.get("/laps/{year}/{grand_prix}/{session_type}/{driver}")
async def driver_laps(year: int, grand_prix: str, session_type: str, driver: str):
    data = get_driver_laps(year, grand_prix, session_type, driver)
    return {"driver": driver, "laps": data}

@router.get("/tyreDegradation/{year}/{grand_prix}/{session_type}/{driver}")
async def tyre_degradation(year: int, grand_prix: str, session_type: str, driver: str):
    data =get_tyre_degradation(year, grand_prix, session_type, driver)
    return data