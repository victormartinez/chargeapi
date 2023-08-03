# type: ignore
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects import postgresql

from chargeapi.db import Base
from chargeapi.db.functions import utcnow


class BaseModel(Base):
    # __abstract__ has to be True for Alembic doesn't create BaseModel as a Table in DB
    __abstract__ = True

    id = Column(
        postgresql.UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    created_at = Column(DateTime(timezone=True), server_default=utcnow())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
    )
