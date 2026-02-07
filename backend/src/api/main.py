from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, tasks
from ..config import settings
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="Todo API",
        description="RESTful API for the Todo application with JWT authentication",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # Allow Authorization header for JWT tokens
        allow_credentials=True,
    )

    # Include routers
    app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
    app.include_router(tasks.router, prefix="/api", tags=["tasks"])

    # Add exception handlers
    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request, exc):
        """Custom handler for HTTP exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        """Custom handler for request validation errors."""
        return JSONResponse(
            status_code=422,
            content={
                "detail": [
                    {
                        "loc": err["loc"],
                        "msg": err["msg"],
                        "type": err["type"]
                    } for err in exc.errors()
                ]
            }
        )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint to verify API is running."""
        return {"status": "healthy", "message": "Todo API is running"}

    return app


# Create the main app instance
app = create_app()


# Main entry point for uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )