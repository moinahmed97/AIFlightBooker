# AI Flight Search Agent

This Python script implements an AI-powered agent that finds the cheapest flight between two specified locations on a given date. It utilizes the Amadeus API for real-time flight data and `pydantic-ai` to structure the interaction with a language model (LLM) like GPT. The agent is also prompted to provide cool facts about the destination city.

## Features

* **Real-time Flight Search:** Connects to the Amadeus API to fetch current flight offers.
* **Cheapest Flight Identification:** Processes search results to find the most affordable option.
* **AI-Powered Interaction:** Uses `pydantic-ai` to manage an agent that processes requests and uses tools.
* **Structured Output:** Defines Pydantic models (`FlightDetails`, `NoFlightFound`) for clear and validated results.
* **Environment Variable Configuration:** Supports `.env` files for managing API keys.
* **Asynchronous Operations:** Built with `asyncio` for efficient I/O operations.
* **Destination Facts:** The AI agent is prompted to also provide interesting facts about the destination.

## Prerequisites

* Python 3.8+
* An Amadeus for Developers account and API Keys (Client ID & Client Secret).
* An API key for an LLM provider compatible with `pydantic-ai` (e.g., OpenAI API Key for GPT models). The script is currently configured for `'gpt-4.1-mini'`.

## Setup

1.  **Clone the repository (or save the script):**
    ```bash
    # If it's in a git repo
    # git clone <repository_url>
    # cd <repository_name>
    ```
    If you just have the script, save it as a `.py` file (e.g., `flight_agent.py`).

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file with the following content:
    ```txt
    pydantic
    pydantic-ai
    amadeus
    python-dotenv
    openai # Or other relevant library for your chosen LLM
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory of your project with your API credentials:
    ```env
    # Amadeus API Credentials
    AMADEUS_CLIENT_ID="YOUR_AMADEUS_CLIENT_ID"
    AMADEUS_CLIENT_SECRET="YOUR_AMADEUS_CLIENT_SECRET"

    # LLM Provider API Key (e.g., OpenAI)
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```
    **Important:** The provided script initializes the Amadeus client with hardcoded placeholder credentials:
    ```python
    amadeus = Client(
        client_id='', # Placeholder
        client_secret=''          # Placeholder
    )
    ```
    You **must** replace these placeholders with your actual Amadeus credentials. For better security and practice, modify the script to load these from environment variables, for example:
    ```python
    import os
    from dotenv import load_dotenv
    load_dotenv() # Loads variables from .env

    amadeus = Client(
        client_id=os.getenv('AMADEUS_CLIENT_ID'),
        client_secret=os.getenv('AMADEUS_CLIENT_SECRET')
    )
    ```
    The `load_dotenv()` call is already present in your script, so you mainly need to adjust the `Client` initialization.

## Usage

To run the script:

```bash
python your_script_name.py
