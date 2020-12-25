import unittest

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import (
    NoResultFound,
    MultipleResultsFound,
)

try:
    import context
except:
    from tests import context
from sqlalchemy_asyncselect import select, delete

Base = declarative_base()


class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data1 = Column(String)
    data2 = Column(String)


class AsyncSelectTestSuite(unittest.IsolatedAsyncioTestCase):
    """test cases."""

    async def asyncSetUp(self):
        self.engine = create_async_engine("sqlite:///:memory:")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async with AsyncSession(self.engine) as session:
            async with session.begin():
                session.add_all(
                    [
                        A(data1="a1", data2="b1"),
                        A(data1="a2", data2="b2"),
                        A(data1="a2", data2="b2"),
                    ]
                )

    async def test_engine(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a1").execute(session)
        self.assertEqual("b1", result.scalars().one().data2)

    async def test_scalars(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a1").scalars(session)
        self.assertEqual("b1", result.one().data2)

    async def test_one(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a1").one(session)
        self.assertEqual("b1", result.data2)

    async def test_one_without_matched_row(self):
        with self.assertRaises(NoResultFound):
            async with AsyncSession(self.engine) as session:
                await select(A).filter_by(data1="a3").one(session)

    async def test_one_with_multiple_rows(self):
        with self.assertRaises(MultipleResultsFound):
            async with AsyncSession(self.engine) as session:
                await select(A).filter_by(data1="a2").one(session)

    async def test_one_or_none(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a1").one_or_none(session)
        self.assertEqual("b1", result.data2)

    async def test_one_or_none_without_matched_row(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a3").one_or_none(session)
        self.assertEqual(None, result)

    async def test_one_or_none_with_multiple_rows(self):
        with self.assertRaises(MultipleResultsFound):
            async with AsyncSession(self.engine) as session:
                await select(A).filter_by(data1="a2").one_or_none(session)

    async def test_first(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a1").first(session)
        self.assertEqual("b1", result.data2)

    async def test_first_without_matched_row(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a3").first(session)
        self.assertEqual(None, result)

    async def test_first_with_multiple_rows(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a2").first(session)
        self.assertEqual("b2", result.data2)

    async def test_fetchmany(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a1").fetchmany(session, size=2)
        self.assertEqual(["b1"], [x.data2 for x in result])

    async def test_fetchmany_without_matched_row(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a3").fetchmany(session, size=2)
        self.assertEqual([], list(result))

    async def test_fetchmany_with_multiple_rows(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a2").fetchmany(session, size=2)
        self.assertEqual(["b2", "b2"], [x.data2 for x in result])

    async def test_all(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a1").all(session)
        self.assertEqual(["b1"], [x.data2 for x in result])

    async def test_all_without_matched_row(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a3").all(session)
        self.assertEqual([], list(result))

    async def test_all_with_multiple_rows(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a2").all(session)
        self.assertEqual(["b2", "b2"], [x.data2 for x in result])

    async def test_fetchall(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a1").fetchall(session)
        self.assertEqual(["b1"], [x.data2 for x in result])

    async def test_fetchall_without_matched_row(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a3").fetchall(session)
        self.assertEqual([], list(result))

    async def test_fetchall_with_multiple_rows(self):
        async with AsyncSession(self.engine) as session:
            result = await select(A).filter_by(data1="a2").fetchall(session)
        self.assertEqual(["b2", "b2"], [x.data2 for x in result])


class AsyncDeleteTestSuite(unittest.IsolatedAsyncioTestCase):
    """test cases."""

    async def asyncSetUp(self):
        self.engine = create_async_engine("sqlite:///:memory:")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async with AsyncSession(self.engine) as session:
            async with session.begin():
                session.add_all(
                    [
                        A(data1="a1", data2="b1"),
                        A(data1="a2", data2="b2"),
                        A(data1="a2", data2="b2"),
                    ]
                )

    async def test_engine(self):
        async with AsyncSession(self.engine) as session:
            await delete(A).filter_by(data1="a1").execute(session)
            result = await select(A).filter_by(data1="a1").one_or_none(session)
        self.assertEqual(None, result)

    async def test_engine_2(self):
        async with AsyncSession(self.engine) as session:
            await delete(A).filter_by(data1="a1").execute(session)
            result = await select(A).all(session)
        self.assertEqual(["b2", "b2"], [x.data2 for x in result])


if __name__ == "__main__":
    unittest.main()
