class DatabaseUtils:
    @classmethod
    async def create(cls, db_session, data) -> None:
        db_session.add(data)
        await db_session.commit()

    @classmethod
    async def create_many(cls, db_session, objects) -> None:
        await db_session.run_sync(lambda session: session.bulk_save_objects(objects))

    @classmethod
    def expire_session_objects(cls, db_session) -> None:
        # expire all objects in the current session to fetch
        # Learn more:
        # https://stackoverflow.com/questions/19143345/about-refreshing-objects-in-sqlalchemy-session
        db_session.expire_all()
