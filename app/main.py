"""Main application entry point."""

from fastapi import FastAPI
from app.api.routes import router

# Create FastAPI app
app = FastAPI(
    title="Greek Nameday API",
    description="Fetches nameday information (celebrating names and saints) from eortologio.net",
    version="1.0.0",
)

# Include API routes
app.include_router(router)

# Run the app if executed directly
if __name__ == "__main__":
    import uvicorn

    print("Starting Uvicorn server. Access API at http://127.0.0.1:8000")
    print("Access Swagger UI documentation at http://127.0.0.1:8000/docs")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
