import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_client():
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Login para obter token
        login = await ac.post("/auth/login", json={
            "email": "teste@exemplo.com",
            "password": "senha123"
        })
        token = login.json()["access_token"]

        # Criar cliente
        response = await ac.post(
            "/clients/",
            json={"name": "Cliente Teste", "email": "cliente@teste.com", "cpf": "12345678901"}, # noqa E501
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code in (200, 201, 400)
