from json import JSONDecodeError
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from chargeapi.api.exception_handlers import (
    bad_request_handler,
    http_exception_handler,
    validation_exception_handler,
)
from chargeapi.api.bank_slips.resources import router as bank_slips_router
from chargeapi.api.debts.resources import router as debts_router
from chargeapi.app.exceptions import ChargeApiException


def create_application() -> FastAPI:
    application = FastAPI()
    configure_healthcheck(application)
    configure_routes(application)
    configure_exception_handlers(application)

    return application


def configure_routes(application: FastAPI) -> None:
    application.include_router(bank_slips_router)
    application.include_router(debts_router)


def configure_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(JSONDecodeError, bad_request_handler)
    application.add_exception_handler(
        ChargeApiException, validation_exception_handler
    )


def configure_healthcheck(app: FastAPI) -> None:
    @app.get("/")
    async def healthcheck() -> Dict[str, Any]:
        return {
            "application": "BankSlip Service",
            "healthy": True,
        }


app = create_application()
