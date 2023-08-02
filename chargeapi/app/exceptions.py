from enum import Enum
from typing import Any, Dict, List, Optional


class ChargeApiExceptionType(Enum):
    DATABASE_ERROR = "DATABASE_ERROR"
    DATABASE_INTEGRITY_ERROR = "DATABASE_INTEGRITY_ERROR"
    ENTITY_NOT_FOUND = "ENTITY_NOT_FOUND"
    ENTITY_INACTIVE = "ENTITY_INACTIVE"


class ChargeApiException(Exception):
    def __init__(
        self,
        type: ChargeApiExceptionType,
        message: str,
        errors: Optional[List[Dict[str, str]]] = None,
    ):
        self.type = type
        self.message = message
        self.errors = errors or []
        super().__init__(message)

    @property
    def data(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "type": self.type,
            "errors": self.errors,
        }
