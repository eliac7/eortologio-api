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

### Prerequisites

- Python 3.11 or higher
- `uv` package manager (recommended) or `pip`

### Installing uv

Choose one of these methods to install `uv`:

```bash
# Using the official installer (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv

# Or using pipx (for isolated installation)
pipx install uv
```

### Project Setup

1. Clone the repository:

```bash
git clone https://github.com/eliac7/eortologio-api.git
cd eortologio-api
```

2. Create and activate a virtual environment:

```bash
# Create a virtual environment with uv
uv venv
# Activate it (Windows)
.venv\Scripts\activate
# Activate it (macOS/Linux)
source .venv/bin/activate
```

3. Install dependencies:

```bash
# Install project dependencies
uv pip install .

# For development dependencies
uv pip install -e ".[dev]"
```

### Docker Setup

1. Build and start the container:

```bash
docker compose up -d
```

The API will be available at http://localhost:8000.

## Development

### Installing Development Dependencies

```bash
uv pip install -e ".[dev]"
```

### Running Tests

```bash
uv run pytest
```

### Running the API Locally

```bash
# Using uvicorn directly
uv run -- uvicorn app.main:app --reload

# Or using the installed script
uv run eortologio-api-server
```

The API will be available at http://127.0.0.1:8000.

### Adding New Dependencies

```bash
# Add a production dependency
uv pip install package-name

# Add a development dependency
uv pip install package-name[dev]
```

### Updating Dependencies

```bash
# Update all dependencies
uv pip install --upgrade .

# Update specific package
uv pip install --upgrade package-name
```

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

- Build and start: `docker compose up -d`
- Stop: `docker compose down`
- View logs: `docker compose logs -f`
- Rebuild: `docker compose up -d --build`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

This API uses data from [eortologio.net](https://www.eortologio.net/) and is intended for personal or educational use only.
