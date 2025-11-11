from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta, time
import os

app = FastAPI()

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI 🚀"}


@app.get("/api/working_hours")
def working_hours(
    start: str = Query(..., description="Start datetime, format YYYY-MM-DDTHH:MM:SS"),
    end: str = Query(..., description="End datetime, format YYYY-MM-DDTHH:MM:SS"),
):
    """
    Calculate working hours between two datetimes.
    Only counts Monday-Friday, hours 08:00-16:00.
    Returns high-precision decimal hours.
    """
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    if end_dt <= start_dt:
        return {"working_hours": 0.0}

    total_hours = 0.0
    current_day = start_dt.date()
    end_day = end_dt.date()

    while current_day <= end_day:
        # Only Monday-Friday
        if current_day.weekday() < 5:
            # Workday start/end
            work_start = datetime.combine(current_day, time(8, 0, 0))
            work_end = datetime.combine(current_day, time(16, 0, 0))

            # Count overlap
            period_start = max(work_start, start_dt)
            period_end = min(work_end, end_dt)

            if period_end > period_start:
                # Add fraction of hours
                total_hours += (period_end - period_start).total_seconds() / 3600.0

        current_day += timedelta(days=1)

    # Round to 2 decimal places for readability
    return {"working_hours": round(total_hours, 3)}