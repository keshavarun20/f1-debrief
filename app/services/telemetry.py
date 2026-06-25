import fastf1
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def resolve_session_type(session_type: str) -> tuple[str, str | None]:
    mapping = {
        'Q1': ('Q', 'Q1'),
        'Q2': ('Q', 'Q2'),
        'Q3': ('Q', 'Q3'),
    }
    return mapping.get(session_type, (session_type, None))

def get_session(year: int, grand_prix: str, session_type: str):
    fastf1_type, _ = resolve_session_type(session_type)
    session = fastf1.get_session(year, grand_prix, fastf1_type)
    session.load()
    return session

def get_driver_laps(year: int, grand_prix: str, session_type: str, driver: str):
    fastf1_type, q_part = resolve_session_type(session_type)
    session = fastf1.get_session(year, grand_prix, fastf1_type)
    session.load()
    laps = session.laps.pick_drivers(driver)

    if q_part and 'Session' in laps.columns:
        laps = laps[laps['Session'] == q_part]

    return laps[["LapNumber", "LapTime", "Sector1Time", "Sector2Time", "Sector3Time", "Compound", "TyreLife"]].to_dict(orient="records")

def get_tyre_degradation(year: int, grand_prix: str, session_type: str, driver: str):
    session = get_session(year, grand_prix, session_type)
    laps = session.laps.pick_drivers(driver)

    laps = laps[laps["PitOutTime"].isna()]
    laps = laps[laps["PitInTime"].isna()]
    laps = laps.dropna(subset=["LapTime", "TyreLife", "LapNumber", "Compound", "Stint"])
    laps = laps.copy()
    laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()

    stints = []

    for stint_number, stint_laps in laps.groupby("Stint"):
        if len(stint_laps) < 3:
            continue

        compound = stint_laps["Compound"].iloc[0]

        stint_median = stint_laps["LapTimeSeconds"].median()
        clean_laps = stint_laps[stint_laps["LapTimeSeconds"] <= stint_median * 1.07]

        if len(clean_laps) < 3:
            continue

        max_tyre_life = int(clean_laps["TyreLife"].dropna().max())

        X = clean_laps[["TyreLife"]].to_numpy()
        y = clean_laps["LapTimeSeconds"].to_numpy(dtype=float)

        model = LinearRegression()
        model.fit(X, y)

        raw_deg = float(model.coef_[0])
        deg_rate = round(max(-0.05, raw_deg), 4)
        base_pace = round(float(model.intercept_), 4)
        r2 = round(float(r2_score(y, model.predict(X))), 3)

        predictions = []
        for tyre_life in range(1, max_tyre_life + 1):
            predicted = base_pace + (deg_rate * tyre_life)
            predictions.append({
                "tyre_life": tyre_life,
                "predicted_lap_time": round(predicted, 4)
            })

        stints.append({
            "stint": int(stint_number),
            "compound": compound,
            "deg_rate_per_lap": deg_rate,
            "base_pace_seconds": base_pace,
            "r_squared": r2,
            "predictions": predictions
        })

    return {
        "driver": driver,
        "stints": stints
    }