"""
Centralized exception handling for the application
"""

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Union


class AppException(Exception):
    """Base exception for application errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class VectorSearchError(AppException):
    """Raised when vector search fails"""
    def __init__(self, message: str = "Vector search failed"):
        super().__init__(message, status_code=500)


class LLMError(AppException):
    """Raised when LLM generation fails"""
    def __init__(self, message: str = "LLM generation failed"):
        super().__init__(message, status_code=500)


class DocumentNotFoundError(AppException):
    """Raised when no relevant documents are found"""
    def __init__(self, message: str = "No relevant documents found"):
        super().__init__(message, status_code=404)


class InvalidInputError(AppException):
    """Raised when user input is invalid"""
    def __init__(self, message: str = "Invalid input"):
        super().__init__(message, status_code=400)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Global handler for application exceptions
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": str(request.url)
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler for unexpected exceptions
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "path": str(request.url)
        }
    )
