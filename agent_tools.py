import re
from .agent import FlightDetails

async def extract_flights(web_page_text: str) -> list[FlightDetails]:
    """
    Extract flight details from web page text using regex.
    Expected format per flight: 
    'Flight AB123 from SFO to LAX on 2025-01-01 for $199'
    """
    pattern = re.compile(
        r"Flight\\s+(?P<flight_number>\\w+)\\s+from\\s+(?P<origin>[A-Z]{3})\\s+to\\s+(?P<destination>[A-Z]{3})\\s+on\\s+(?P<date>\\d{4}-\\d{2}-\\d{2})\\s+for\\s+\\$(?P<price>\\d+)",
        re.IGNORECASE
    )
    flights = []
    for match in pattern.finditer(web_page_text):
        flights.append(
            FlightDetails(
                flight_number=match.group("flight_number"),
                price=int(match.group("price")),
                origin=match.group("origin").upper(),
                destination=match.group("destination").upper(),
                date=match.group("date")
            )
        )
    return flights