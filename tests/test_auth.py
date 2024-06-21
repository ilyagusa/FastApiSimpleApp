import time

from sqlalchemy import insert, select

from auth.models import role
from conftest import client, async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        stat = insert(role).values(id=1, name="admin", permissions=None)
        await session.execute(stat)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, 'admin', None)], "Не удалось добавить роль"


def test_register():
    response = client.post('/auth/register', json={
        "email": "aaa@aaa.ru",
        "password": "password",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "id": 0,
        "username": "Qwerty1",
        "role_id": 1
    })

    assert response.status_code == 201
