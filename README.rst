SQLAlchemy AsyncSelect
======================

Sugar syntax of select/delete wrapper for SQLAlchemy AsyncSelect.

In [the SQLAlchemy document](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncScalarResult),
the original API usage is like::

    async with AsyncSession(self.engine) as session:
        stmt = select(A).options(selectinload(A.bs))
        result = await session.execute(stmt)
        for a1 in result.scalars():
            print(a1)

        result = await session.execute(select(A).order_by(A.id))
        a1 = result.scalars().first()
        a1.data = "new data"
        await session.commit()

Using this wrapper::

    async with AsyncSession(self.engine) as session:
        for a1 in await select(A).options(selectinload(A.bs)).scalar(session):
            print(a1)

        a1 = await select(A).order_by(A.id).first(session)
        a1.data = "new data"
        await session.commit()
