from __future__ import annotations
import asyncio
from dataclasses import dataclass
from typing import Union
from pydantic import BaseModel, Field

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.usage import Usage, UsageLimits

class FlightDetails(BaseModel):
    """Details of the flight."""
    flight_number: str
    price: int
    origin: str = Field(description='Three-letter airport code')
    destination: str = Field(description='Three-letter airport code')
    date: str  # Flight date as a string in YYYY-MM-DD format

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
    'openai:gpt-4o',
    result_type=Union[FlightDetails, NoFlightFound],
    system_prompt='Find the cheapest flight for the user on the given date.'
)

@search_agent.tool
async def search_flights(ctx: RunContext[Deps]) -> FlightDetails | NoFlightFound:
    """Search for flights based on provided dependencies."""
    # Simulate flight search logic or call an external service
    if ctx.deps.req_origin and ctx.deps.req_destination:
        # Dummy data for example
        return FlightDetails(
            flight_number="AB123",
            price=199,
            origin=ctx.deps.req_origin,
            destination=ctx.deps.req_destination,
            date=ctx.deps.req_date
        )
    return NoFlightFound(error="Invalid request.")

async def main():
    deps = Deps(
        web_page_text="dummy_text",
        req_origin="SFO",
        req_destination="LAX",
        req_date="2025-01-01"
    )
    result = await search_agent.run(
        f"Find me a flight from {deps.req_origin} to {deps.req_destination} on {deps.req_date}",
        deps=deps
    )
    print(result)

if __name__ == '__main__':
    asyncio.run(main())