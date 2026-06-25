import httpx

async def get_driver_info(driver_code: str, year: int):
    async with httpx.AsyncClient() as client:

        # Step 1 — get a session key for that year
        sessions_r = await client.get(
            "https://api.openf1.org/v1/sessions",
            params={"year": year, "session_type": "Race"}
        )
        sessions = sessions_r.json()

        if not sessions or not isinstance(sessions, list):
            return None

        session_key = sessions[0]["session_key"]

        # Step 2 — get driver using session key + acronym
        drivers_r = await client.get(
            "https://api.openf1.org/v1/drivers",
            params={
                "name_acronym": driver_code.upper(),
                "session_key": session_key
            }
        )
        data = drivers_r.json()

        if not data or not isinstance(data, list) or len(data) == 0:
            return None

        d = data[0]
        return {
            "full_name": d.get("full_name"),
            "team": d.get("team_name"),
            "number": d.get("driver_number"),
            "headshot_url": d.get("headshot_url"),
            "country_code": d.get("country_code"),
            "team_colour": f"#{d.get('team_colour', 'ffffff')}",
        }