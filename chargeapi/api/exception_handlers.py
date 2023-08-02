from json import JSONDecodeError

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from chargeapi.app.exceptions import ChargeApiException

from .response_handlers import (
    error_to_response,
    http_exception_to_response,
    json_decode_to_response,
)


async def validation_exception_handler(
    request: Request, exc: ChargeApiException
) -> JSONResponse:
    body = error_to_response(exc)
    return JSONResponse(status_code=body.code, content=body.dict())


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    body = http_exception_to_response(exc)
    return JSONResponse(status_code=body.code, content=body.dict())


async def bad_request_handler(
    request: Request,
    exc: JSONDecodeError,
) -> JSONResponse:
    body = json_decode_to_response(exc)
    return JSONResponse(status_code=body.code, content=body.dict())
