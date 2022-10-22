# from .session import async_db_session as session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete, exists


class DBMixin:
    @classmethod
    async def _execute_query(cls, query, session):
        try:
            result = await session.execute(query)
        except Exception as e:
            raise e
        else:
            return result
        finally:
            await session.close()

    @classmethod
    async def create(cls, session, **kwargs):
        new_object = cls(**kwargs)
        session.add(new_object)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
        else:
            return new_object.__dict__
        finally:
            await session.close()

    @classmethod
    async def get_all(cls, session):
        query = select(cls)
        result = await DBMixin._execute_query(query, session)
        result = [i[0] for i in result.all()]
        return result

    @classmethod
    async def update(cls, id, session, **kwargs):
        query = (
            update(cls).where(cls.id == id).values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        result = await DBMixin._execute_query(query, session)
        result = result.one_or_none()
        return result

    @classmethod
    async def get_by_id(cls, id, session):
        query = select(cls).where(cls.id == id)
        result = await DBMixin._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0]

    @classmethod
    async def delete(cls, id, session):
        query = delete(cls).where(cls.id == id)
        result = await DBMixin._execute_query(query, session)
        return {'success': True}

    @classmethod
    async def exists(cls, id, session):
        query = exists(cls).where(cls.id == id)
        result = await DBMixin._execute_query(query, session)

    __mapper_args__ = {"eager_defaults": True}
