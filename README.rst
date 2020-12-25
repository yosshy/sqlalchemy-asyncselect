SQLAlchemy AsyncSelect
======================

Sugar syntax of select/delete functions of SQLAlchemy, especially asyncio.

In `SQLAlchemy document`_ , the original Asyncio API of SQLAlchemy is like below::

    engine = create_async_engine("sqlite:///:memory:")
    
    async with AsyncSession(engine) as session:
        stmt = select(A).options(selectinload(A.bs))
        result = await session.execute(stmt)
        for a1 in result.scalars():
            print(a1)
    
        result = await session.execute(select(A).order_by(A.id))
        a1 = result.scalars().first()
        a1.data = "new data"
        await session.commit()

but with this wrapper::

    from sqlalchemy_asyncselect import select, delete

    engine = create_async_engine("sqlite:///:memory:")

    async with AsyncSession(engine) as session:
        for a1 in await select(A).options(selectinload(A.bs)).scalar(session):
            print(a1)
    
        a1 = await select(A).order_by(A.id).first(session)
        a1.data = "new data"
        await session.commit()

And also, deleting row is like below::

    async with AsyncSession(engine) as session:
        stmt = delete(A).filter_by(data="a2")
        await session.execute(stmt)

but with this wrapper::

    async with AsyncSession(engine) as session:
        await delete(A).filter_by(data="a2").execute(session)

_`SQLAlchemy document`: https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncScalarResult
