from httpx import AsyncClient


async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post("/operations/", json={
        "quantity": "25.5",
        "figi": "figi_CDOE",
        "instrument_type": "Купон",
        "date": "2024-06-06 14:09:50.27",
        "type": "Выплата купонов"
    })

    print(response)

    assert response.status_code == 200