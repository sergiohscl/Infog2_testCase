import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from pathlib import Path

transport = ASGITransport(app=app, raise_app_exceptions=True)


@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Primeiro: login
        login = await ac.post("/auth/login", json={
            "email": "teste@exemplo.com",
            "password": "senha123"
        })
        assert login.status_code == 200
        token = login.json()["access_token"]

        # Caminho de uma imagem de teste
        image_path = Path(__file__).parent / "test_image.jpg"
        if not image_path.exists():
            # cria uma imagem falsa temporária
            image_path.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")

        # Envio do formulário de produto com imagem
        with image_path.open("rb") as img_file:
            response = await ac.post(
                "/products/",
                headers={"Authorization": f"Bearer {token}"},
                files={"imagem": ("test_image.jpg", img_file, "image/jpeg")},
                data={
                    "nome_produto": "Produto Teste",
                    "descricao": "Descrição de teste",
                    "preco_venda": "99.90",
                    "estoque": "5",
                    "validade": "31-12-2025",
                    "disponivel": "true"
                }
            )

        assert response.status_code == 200 or response.status_code == 201
        json = response.json()
        assert json["nome_produto"] == "Produto Teste"
        assert json["preco_venda"] == 99.90
        assert json["imagem"].startswith("/static/img/")
