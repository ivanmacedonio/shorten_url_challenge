from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from app.adapters.input.api.controllers import url_router, user_router, auth_router
from app.domain.utils.rate_limiter import limiter, custom_rate_limit_handler

# Mount main app
app = FastAPI()

# Limit max rate
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)

# Health check route
@app.get("/health", tags=["Health"])
@limiter.limit("3/minute")
def health_check(request: Request):
    return {"status": "ok"}

# Mount routers
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(url_router.router, prefix="/urls", tags=["Urls"])
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
