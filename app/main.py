from fastapi import FastAPI
from app.adapters.input.api.controllers import url_router, user_router

# Mount main app
app = FastAPI()

# Health check route
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

# Mount routers
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(url_router.router, prefix="/urls", tags=["Urls"])
