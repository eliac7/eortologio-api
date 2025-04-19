from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routes import router
from app.core.rate_limit import limiter

app = FastAPI(
    title="Greek Nameday API",
    description="Fetches nameday information (celebrating names and saints) from eortologio.net",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    print("Starting Uvicorn server. Access API at http://127.0.0.1:8000")
    print("Access Swagger UI documentation at http://127.0.0.1:8000/docs")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
