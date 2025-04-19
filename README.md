# Greek Nameday API

A FastAPI-based API for fetching Greek nameday information from eortologio.net.

## Features

- Get today's and tomorrow's namesday information
- Get nameday information for the current or a specific month
- Search for celebration dates of specific names
- Response caching for improved performance

## Project Structure

```
eortologio-api/
│
├── app/                    # Main application package
│   ├── api/                # API routes
│   │   ├── __init__.py
│   │   └── routes.py       # API endpoint definitions
│   │
│   ├── core/               # Core application components
│   │   ├── __init__.py
│   │   └── config.py       # Configuration settings
│   │
│   ├── models/             # Data models
│   │   ├── __init__.py
│   │   └── schemas.py      # Pydantic models for API schemas
│   │
│   ├── services/           # Business logic services
│   │   ├── __init__.py
│   │   ├── cache.py        # Caching implementation
│   │   └── nameday_service.py  # Nameday data fetching and parsing
│   │
│   ├── utils/              # Utility functions
│   │   ├── __init__.py
│   │   └── http.py         # HTTP request utilities
│   │
│   ├── __init__.py
│   └── main.py             # FastAPI application instance
│
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore           # Docker ignore file
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Installation

### Traditional Setup

1. Clone the repository:

```bash
git clone https://github.com/eliac7/eortologio-api.git
cd eortologio-api
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Docker Setup

1. Clone the repository:

```bash
git clone https://github.com/eliac7/eortologio-api.git
cd eortologio-api
```

2. Build and start the Docker container:

```bash
docker-compose up -d
```

The API will be available at http://localhost:8000.

## Usage

### Running the API Locally

```bash
# From the project root directory
uvicorn app.main:app --reload

# Or using the Python module
python -m app.main
```

The API will be available at http://127.0.0.1:8000.

### API Documentation

Once the application is running, you can access:

- Interactive API documentation (Swagger UI): http://127.0.0.1:8000/docs
- Alternative API documentation (ReDoc): http://127.0.0.1:8000/redoc

### API Endpoints

- `GET /`: API health check
- `GET /today`: Get today's nameday information
- `GET /tomorrow`: Get tomorrow's nameday information
- `GET /month`: Get nameday information for the current month
- `GET /month/{month_num}`: Get nameday information for a specific month (1-12)
- `GET /search/{name}`: Search celebration dates for a specific name

## Docker Commands

- Start the container: `docker-compose up -d`
- Stop the container: `docker-compose down`
- View logs: `docker-compose logs -f`
- Rebuild the container: `docker-compose up -d --build`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

This API uses data from [eortologio.net](https://www.eortologio.net/) and is intended for personal or educational use only.
