from __future__ import annotations
import asyncio
from dataclasses import dataclass
from typing import Union
from pydantic import BaseModel, Field

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.usage import Usage, UsageLimits
from amadeus import Client, ResponseError

# Initialize the Amadeus client (put your real credentials here)
amadeus = Client(
    client_id='',
    client_secret=''
)

def get_real_flights(origin, destination, date):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=date,
            adults=1
        )
        return response.data  # This is a list of flight offers
    except ResponseError as error:
        print(error)
        return []
from dotenv import load_dotenv
load_dotenv()

class FlightDetails(BaseModel):
    """Details of the flight."""
    flight_number: str
    price: float
    origin: str = Field(description='Three-letter airport code')
    destination: str = Field(description='Three-letter airport code')
    date: str  # Flight date as a string in YYYY-MM-DD format# Flight date as a string in YYYY-MM-DD format

class NoFlightFound(BaseModel):
    """Indicates no valid flight is found."""
    error: str

@dataclass
class Deps:
    web_page_text: str
    req_origin: str
    req_destination: str
    req_date: str

search_agent = Agent[Deps, Union[FlightDetails, NoFlightFound]](
    'gpt-4.1-mini',
    result_type=Union[FlightDetails, NoFlightFound],
    system_prompt='Find the cheapest flight for the user on the given date and tell them cool facts about their destination .'
)

@search_agent.tool
async def search_flights(ctx: RunContext[Deps]) -> FlightDetails | NoFlightFound:
    flights = get_real_flights(ctx.deps.req_origin, ctx.deps.req_destination, ctx.deps.req_date)
    if flights:
        # Extract the cheapest flight and format as FlightDetails
        cheapest = min(flights, key=lambda f: float(f['price']['total']))
        return FlightDetails(
            flight_number=cheapest['itineraries'][0]['segments'][0]['carrierCode'] + cheapest['itineraries'][0]['segments'][0]['number'],
            price=(float(cheapest['price']['total'])),
            origin=ctx.deps.req_origin,
            destination=ctx.deps.req_destination,
            date=ctx.deps.req_date
        )
    return NoFlightFound(error="No flights found for the given criteria.")

async def main():
    deps = Deps(
        web_page_text="Flight AB123 from SFO to LAX on 2025-01-01 for $199\nFlight XY456 from SFO to LAX on 2025-01-01 for $150",
        req_origin="SFO",
        req_destination="LAX",
        req_date="2025-05-05"
    )
    result = await search_agent.run(
        f"Find me a flight from {deps.req_origin} to {deps.req_destination} on {deps.req_date}",
        deps=deps
    )
    # --- Begin output formatting ---
    # If using pydantic_ai >= 0.4.0, result.data is the actual output
    flight = getattr(result, "data", result)
    if hasattr(flight, "flight_number"):
        print(f"Cheapest flight found:\n"
              f"  Flight Number: {flight.flight_number}\n"
              f"  Origin: {flight.origin}\n"
              f"  Destination: {flight.destination}\n"
              f"  Date: {flight.date}\n"
              f"  Price: ${flight.price}")
    elif hasattr(flight, "error"):
        print(f"No flight found: {flight.error}")
    else:
        print("Unexpected result:", flight)
    # --- End output formatting ---

if __name__ == '__main__':
    asyncio.run(main())