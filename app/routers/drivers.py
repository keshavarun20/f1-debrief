from fastapi import APIRouter

from app.services.drivers import get_driver_info

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.get("/{year}/{driver_code}")
async def driver_info(year: int, driver_code: str):
    data = await get_driver_info(driver_code, year)
    if not data:
        return {"error": "Driver not found"}
    return data