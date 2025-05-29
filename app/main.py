from fastapi import FastAPI

from app.routes import auth_routes

app = FastAPI(
    title="Auth & User Service",
    description="Python FastAPI backend authentication, authorization, and use service",
    version="1.0.0"
)

# Include routers
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Auth service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 