import datetime
import zoneinfo
from typing import Optional

from db import create_all_tables
from fastapi import Depends, FastAPI, HTTPException, Request, security
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .routers import customers, invoices, plans, transactions

app = FastAPI(lifespan=create_all_tables)

routers = [customers.router, transactions.router, invoices.router, plans.router]
for router in routers:
    app.include_router(router)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = datetime.datetime.now()
    response = await call_next(request)
    process_time = (datetime.datetime.now() - start_time).total_seconds()
    print(f"Request processed in {process_time:.6f} seconds")
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.middleware("http") 
async def log_request_headers(request: Request, call_next):
    
    print("--------------------")
    print("Request Headers:")
    for header, value in request.headers.items():
        print(f"{header}: {value}")

    response = await call_next(request) 
    print("--------------------")

    return response


security = security.HTTPBasic()

@app.get("/")
async def root(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == 'admin' and credentials.password == 'password':
        return {"message": "Hello Admin"}
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing credentials")
    if credentials.username != "admin" or credentials.password != "password":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "Hello World"}
    

country_timezones = {
    "USA": "America/New_York",
    "UK": "Europe/London",
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "BR": "America/Sao_Paulo",
}

def get_time_in_timezone(iso_code: str, format_time_code: str = "12") -> dict:
    """
    This function retrieves the current time in a specified timezone based on the provided ISO code.

    Parameters:
    iso_code (str): A string representing the ISO code of the desired timezone.
    format_time_code (str, optional): A string representing the desired format of the time. Defaults to "12" (12-hour format).

    Returns:
    dict: A dictionary containing the current time in the specified timezone, or an error message if the ISO code is invalid or the format time code is invalid.
    """
    try:
        iso = iso_code.upper()
        timezone = country_timezones.get(iso)

        if timezone is None:
            raise ValueError("Invalid ISO code")

        tz = zoneinfo.ZoneInfo(timezone)

        if format_time_code not in ["24", "12"]:
            raise ValueError("Invalid format time code")

        if format_time_code == "24":
            return {"time": datetime.datetime.now(tz).strftime("%H:%M:%S")}

        return {"time": datetime.datetime.now(tz).strftime("%I:%M:%p")}

    except Exception as e:
        return {"error": str(e)}

@app.get("/time/{iso_code}")
async def time_endpoint(iso_code: str, format_time_code: Optional[str] = "12"):
    return get_time_in_timezone(iso_code, format_time_code)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
