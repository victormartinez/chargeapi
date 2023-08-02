from chargeapi.db import Base


class BaseModel(Base):
    # __abstract__ has to be True for Alembic doesn't create BaseModel as a Table in DB
    __abstract__ = True
