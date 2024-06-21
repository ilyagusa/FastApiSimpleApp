import time

from fastapi import APIRouter, Depends

from fastapi_cache.decorator import cache

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from operations.models import operation
from operations.schemas import OperationCreate

router = APIRouter(prefix="/operations", tags=["Operation"])


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    stmt = select(operation).where(operation.c.type == operation_type)
    print(stmt)
    result = await session.execute(stmt)
    print(result)

    return result.mappings().all()


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    res = {"status": "success", "status_code": 200}

    try:
        stmt = insert(operation).values(**new_operation.dict())
        print(stmt)
        await session.execute(stmt)
        await session.commit()
    except Exception as ex:
        res = {"status": "error", "details": str(ex), "status_code": 400}

    return res


@router.get("/long_operation")
@cache(expire=30)
async def long_operation():
    time.sleep(5)
    return "You get result"
