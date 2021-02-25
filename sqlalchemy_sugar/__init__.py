from typing import List

from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult, AsyncScalarResult
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql.dml import Delete
from sqlalchemy.sql.selectable import Select
from sqlalchemy.util.langhelpers import public_factory


__all__ = ["delete", "select"]


class AsyncSelect(Select):
    async def execute(self, session: AsyncSession) -> AsyncResult:
        """Execute a statement and return a buffered AsyncResult object.

        Args:
            session: Asyncio version of Session.
        Returns:
            A buffered AsyncResult object.
        """
        return await session.execute(self)

    async def scalars(self, session: AsyncSession) -> AsyncScalarResult:
        """Execute a statement and return a buffered AsyncScalarResult object.

        Args:
            session: Asyncio version of Session.
        Returns:
            A buffered AsyncScalarResult object.
        """
        return (await session.execute(self)).scalars()

    async def one(self, session: AsyncSession) -> DeclarativeMeta:
        """Return exactly one object or raise an exception.

        Args:
            session: Asyncio version of Session.
        Returns:
            A scalar value.
        Raises:
            MultipleResultsFound: multiple values are found
            NoResultFound: no value is found
        """
        return (await session.execute(self)).scalars().one()

    async def one_or_none(self, session: AsyncSession) -> DeclarativeMeta:
        """Return at most one object or raise an exception.

        Args:
            session: Asyncio version of Session.
        Returns:
            A scalar value.
        Raises:
            MultipleResultsFound: multiple values are found
        """
        return (await session.execute(self)).scalars().one_or_none()

    async def first(self, session: AsyncSession) -> DeclarativeMeta:
        """Fetch the first object or None if no object is present.

        Args:
            session: Asyncio version of Session.
        Returns:
            A scalar value.
        """
        return (await session.execute(self)).scalars().first()

    async def fetchmany(
        self, session: AsyncSession, size: int
    ) -> List[DeclarativeMeta]:
        """Iterate through sub-lists of elements of the size given.

        Args:
            session: Asyncio version of Session.
            size: max length of the result list.
        Returns:
            List of scalar values.
        """
        return (await session.execute(self)).scalars().fetchmany(size=size)

    async def all(self, session: AsyncSession) -> List[DeclarativeMeta]:
        """Return all scalar values in a list.

        Args:
            session: Asyncio version of Session.
        Returns:
            List of scalar values.
        """
        return (await session.execute(self)).scalars().all()

    fetchall = all


class AsyncDelete(Delete):
    async def execute(self, session: AsyncSession) -> AsyncResult:
        """Execute a statement and return a buffered AsyncResult object.

        Args:
            session: Asyncio version of Session.
        Returns:
            A buffered AsyncResult object.
        """
        return await session.execute(self)


select = public_factory(AsyncSelect._create_future_select, ".future.select")
delete = public_factory(AsyncDelete, ".sql.expression.delete")
