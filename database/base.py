from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete, exists
from sqlalchemy.orm import joinedload


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
            await session.refresh(new_object)
        except IntegrityError as e:
            await session.rollback()
            raise e
        else:
            return new_object

    @classmethod
    async def get_all(cls, session):
        query = select(cls)
        result = await cls._execute_query(query, session)
        result = [i[0] for i in result.all()]
        return result

    def _update_row_values(self, **kwargs):
        for key, value in kwargs.items():
            if value is None:
                continue
            setattr(self, key, value)

    @classmethod
    async def update(cls, id: int, session, **kwargs):
        try:
            obj = await cls.get_by_id(id, session)
            cls._update_row_values(obj, **kwargs)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            # you have to manually close session otherwise test will throw RuntimeError (cause unknown)
            await session.close()
        except Exception as e:
            raise e
        else:
            return obj

    @classmethod
    async def get_by_id(cls, id, session):
        query = select(cls).where(cls.id == id)
        result = await cls._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0]

    @classmethod
    async def delete(cls, id, session):
        try:
            obj = await cls.get_by_id(id, session)
            await session.delete(obj)
            await session.commit()
        except Exception as e:
            raise e

    @classmethod
    async def exists(cls, id, session):
        query = exists(cls).where(cls.id == id)
        result = await cls._execute_query(query, session)
        return True if result else False

    @classmethod
    def list_of_fields(cls, fields: list[str]):
        ret = []
        for field in fields:
            f = getattr(cls, field)
            ret.append(joinedload(f))
        return ret

    __mapper_args__ = {"eager_defaults": True}
