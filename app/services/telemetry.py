import fastf1
from app.core import config
from sklearn.linear_model import LinearRegression

def get_session(year: int, grand_prix: str, session_type: str):
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()
    return session

def get_driver_laps(year: int, grand_prix: str, session_type: str, driver: str):
    session = get_session(year, grand_prix, session_type)
    laps = session.laps.pick_drivers(driver)
    return laps[["LapNumber", "LapTime", "Sector1Time", "Sector2Time", "Sector3Time", "Compound", "TyreLife"]].to_dict(orient="records")

def get_tyre_degradation(year: int, grand_prix: str, session_type: str, driver: str):
    session = get_session(year, grand_prix, session_type)
    laps = session.laps.pick_drivers(driver)

    # Clean data - remove outlier laps
    laps = laps[laps["PitOutTime"].isna()]   # remove pit out laps
    laps = laps[laps["PitInTime"].isna()]    # remove pit in laps
    laps = laps.dropna(subset=["LapTime", "TyreLife", "LapNumber"])

    # Convert LapTime from timedelta to seconds
    laps = laps.copy()
    laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()

    # Define X and y
    X = laps[["TyreLife", "LapNumber"]].to_numpy()
    y = laps["LapTimeSeconds"].to_numpy(dtype=float)

    # Fit model
    model = LinearRegression()
    model.fit(X, y)

    deg_rate = round(float(model.coef_[0]), 4)
    fuel_effect = round(float(model.coef_[1]), 4)
    base_pace = round(float(model.intercept_), 4)   # base lap time in seconds

    return {
        "driver": driver,
        "deg_rate_per_lap": deg_rate,
        "fuel_effect_per_lap": fuel_effect,
        "base_pace_seconds": base_pace,
    }