from enum import Enum
from http import HTTPStatus
from json import JSONDecodeError
from typing import Dict, List, Optional

from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from chargeapi.app.exceptions import ChargeApiException, ChargeApiExceptionType


class ErrorData(BaseModel):
    reason: str
    message: str
    location: str


class ResponseBody(BaseModel):
    message: str = ""
    type: str = ""
    code: HTTPStatus
    errors: Optional[List[ErrorData | Dict]] = None


def _get_error_code(err_type: Enum) -> HTTPStatus:
    return {  # type: ignore
        ChargeApiExceptionType.DATABASE_ERROR: HTTPStatus.INTERNAL_SERVER_ERROR,
        ChargeApiExceptionType.DATABASE_INTEGRITY_ERROR: HTTPStatus.CONFLICT,
        ChargeApiExceptionType.ENTITY_NOT_FOUND: HTTPStatus.NOT_FOUND,
    }.get(err_type, HTTPStatus.INTERNAL_SERVER_ERROR)


def error_to_response(exc: ChargeApiException) -> ResponseBody:
    exception_data = exc.data
    return ResponseBody(
        message=exception_data["message"],
        type=exception_data["type"].value,
        code=_get_error_code(exception_data["type"]),
        errors=exception_data["errors"],
    )


def json_decode_to_response(exc: JSONDecodeError) -> ResponseBody:
    return ResponseBody(
        message="There was an error parsing JSON",
        code=HTTPStatus.BAD_REQUEST,
        type="JSONDecodeError",
        errors=[vars(exc)],
    )


def http_exception_to_response(exc: HTTPException) -> ResponseBody:
    return ResponseBody(
        type="HTTPException",
        code=HTTPStatus(exc.status_code),
        errors=[{"detail": exc.detail}],
    )
