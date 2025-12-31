
from fastapi import FastAPI, Request,status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from backend.app.logging import logger

async def fallback_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "unexpected.server_error",
        extra={
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error occurred,server state invalid or inconsistent ",
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = exc.errors()

    messages = [err.get("msg", "Invalid value") for err in errors]

    logger.warning(
        "request.validation_failed",
        extra={
            "path": request.url.path,
            "method": request.method,
            "errors": errors, 
        },
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": messages[0] if messages else "Invalid request payload",
        },
    )

def register_all_exceptions(app: FastAPI) -> None:
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        fallback_handler,
    )

 