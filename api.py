from fastapi import FastAPI, Query
from agent import search_flights, Deps  # Import from your existing code

app = FastAPI()

@app.get("/search")
async def search(
    origin: str = Query(...),
    destination: str = Query(...),
    date: str = Query(...)
):
    deps = Deps(
        web_page_text="",  # You can adjust this as needed
        req_origin=origin,
        req_destination=destination,
        req_date=date
    )
    result = await search_flights(deps)
    return result.dict()