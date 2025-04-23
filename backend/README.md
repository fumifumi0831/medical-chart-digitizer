# Medical Chart Digitizer - Backend Service

This is the FastAPI backend service for the Medical Chart Digitizer system.

## Setup

### Using Docker

```bash
docker-compose up backend
```

### Manual Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables (see .env.example)

4. Run the application:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /api/v1/charts` - Upload chart image
- `GET /api/v1/charts/{chart_id}/status` - Check processing status
- `GET /api/v1/charts/{chart_id}` - Get processed results
- `GET /api/v1/charts/{chart_id}/csv` - Download results as CSV

For detailed API documentation, access the Swagger UI at `/docs` when the server is running.