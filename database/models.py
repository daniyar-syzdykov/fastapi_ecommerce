from sqlalchemy import Integer, String, Column, ForeignKey, MetaData, Boolean, update, delete, select
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from .session import async_db_session as session
from . import Base


class DBMixin:
    @classmethod
    async def create(cls, **kwargs):
        new_object = cls(**kwargs)
        session.add(new_object)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
        finally:
            await session.close()
        return new_object.__dict__

    @classmethod
    async def get_all(cls):
        query = select(cls)
        result = None
        try:
            result = await session.execute(query)
        except Exception as e:
            print('This exception ocured -----> ', e)
        else:
            result = [i[0] for i in result.all()]
        finally:
            await session.close()
        return result

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            update(cls).where(cls.id == id).values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(query)
        result = [i[0] for i in result.all()]
        await session.commit()
        await session.close()

    @classmethod
    async def get_by_id(cls, id):
        query = select(cls).where(cls.id == id)
        result = await session.execute(query)
        if result is None:
            return None
        result = result.one_or_none()
        await session.close()
        return result[0] if result else None

    @classmethod
    async def delete(cls, id):
        """no idea what to do with this method"""
        query = delete(cls).where(cls.id == id)
        result = await session.execute(query)
        await session.close()
        return {'success': True}

    __mapper_args__ = {"eager_defaults": True}


class Customer(Base, DBMixin):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    username = Column(String(255), unique=True)
    # cart = Column()
    # wish_list = Column()
