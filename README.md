# Port Tariff Calculator

A solution for calculating port tariffs in South African ports using a RAG (Retrieval Augmented Generation) system.

## Features

- Calculate six different types of port tariffs:
  - Light dues
  - Port dues
  - Towage dues
  - Vehicle traffic services (VTS) dues
  - Pilotage dues
  - Running of vessel lines dues
- Support for three South African ports: Durban, Saldanha, and Richards Bay
- Text-based input for maximum flexibility
- RESTful API endpoint for integrating with other systems
- User-friendly Streamlit interface

## Architecture

- **Backend**: FastAPI application that exposes a REST API
- **Frontend**: Streamlit UI for user interaction
- **Core**: RAG system built with LangChain that processes the tariff calculations

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-port-tariff-calculator.git
   cd ai-port-tariff-calculator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create a `.env` file in the root directory):
   ```
   # Add your API keys and configuration here
   GOOGLE_API_KEY=
   COHERE_API_KEY=
   ```

## Running the Application with Docker

The easiest way to deploy the application is using Docker Compose:

1. Make sure Docker and Docker Compose are installed on your system
2. Set environment variables in your `.env` file. You can use `.env.examle` as a template.
3. Build and start the containers:
   ```bash
   docker compose up -d --build
   ```
4. Access the application:
   - Backend API: http://localhost:8000
   - Streamlit UI: http://localhost:8501 - wait for the Backend to start before sending queries

To stop the application:
```bash
docker compose down
```

For viewing logs:
```bash
docker compose logs -f
```

## Running the Application Manually

### Start the FastAPI Server

```bash
python3 -m app.server
```

The API will be available at `http://localhost:8000`.

### Start the Streamlit Frontend

```bash
streamlit run streamlit_app.py
```

The UI will be accessible at `http://localhost:8501`.

## API Documentation

Once the FastAPI server is running, you can access the auto-generated API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

#### `POST /calculate`

Calculates port tariffs for a vessel based on a text query.

**Request Body:**

```json
{
  "query": "Calculate the different tariffs payable by the following vessel berthing at the port of Durban: Vessel Details: General Vessel Name: SUDESTADA Built: 2010 Flag: MLT - Malta..."
}
```

**Response:**

```json
{
  "result": "Light Dues: ZAR 60,062.04\nPort Dues: ZAR 199,549.22\nTowage Dues: ZAR 147,074.38\nVTS Dues: ZAR 33,315.75\nPilotage Dues: ZAR 47,189.94\nVessel Lines Dues: ZAR 19,639.50\nTotal: ZAR 506,830.83"
}
```

## Using the Streamlit Interface

1. Open the Streamlit app at `http://localhost:8501`
2. Enter your query in the text area following the format:
   ```
   Calculate the different tariffs payable by the following vessel berthing at the port of [PORT_NAME]:
   
   [VESSEL_DETAILS]
   ```
3. Click "Calculate Tariffs"
4. View the results in text format
5. Optionally download the results as a text file

## Query Format

Your query should contain sufficient information about the vessel and include the port name. The example query provided in the interface can be used as a template.

**Required information includes:**
- Port name (Durban, Saldanha, or Richards Bay)
- Vessel name
- Main vessel dimensions (GT, NT, LOA, etc.)
- Cargo details
- Activity details

## Example Query

The application comes pre-filled with an example query for the SUDESTADA vessel berthing at the port of Durban. The expected tariff values for this vessel are:

- Light dues: ZAR 60,062.04
- Port dues: ZAR 199,549.22
- Towage dues: ZAR 147,074.38
- Vehicle traffic services (VTS) dues: ZAR 33,315.75
- Pilotage dues: ZAR 47,189.94
- Running of vessel lines dues: ZAR 19,639.50

## License

[MIT License](LICENSE)
