import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_register_and_login():
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Registrar novo usuário
        response = await ac.post("/auth/register", json={
            "name": "Usuário Teste",
            "email": "teste@exemplo.com",
            "password": "senha123"
        })
        assert response.status_code == 200 or response.status_code == 400

        # Fazer login
        response = await ac.post("/auth/login", json={
            "email": "teste@exemplo.com",
            "password": "senha123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
