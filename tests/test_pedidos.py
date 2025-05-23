import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

transport = ASGITransport(app=app, raise_app_exceptions=True)


@pytest.mark.asyncio
async def test_criar_e_consultar_pedido():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Login
        login = await ac.post("/auth/login", json={
            "email": "teste@exemplo.com",
            "password": "senha123"
        })
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Buscar cliente (assumindo cliente id 1 existe)
        cliente_id = 1

        # Buscar 2 produtos disponíveis
        produtos_resp = await ac.get("/products/", headers=headers)
        produtos = produtos_resp.json()
        produtos_ids = [p["id"] for p in produtos if p["estoque"] > 0][:2]
        assert len(produtos_ids) > 0, "Nenhum produto com estoque disponível."

        # Criar pedido
        pedido_resp = await ac.post(
            "/pedidos/",
            json={"cliente_id": cliente_id, "produtos_ids": produtos_ids},
            headers=headers
        )
        assert pedido_resp.status_code == 201
        pedido = pedido_resp.json()

        assert "id" in pedido
        assert pedido["cliente_id"] == cliente_id
        assert pedido["status"] == "aguardando"
        assert set(pedido["produtos_ids"]) == set(produtos_ids)

        pedido_id = pedido["id"]

        # Buscar pedido
        get_resp = await ac.get(f"/pedidos/{pedido_id}", headers=headers)
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == pedido_id

        # Atualizar status
        put_resp = await ac.put(
            f"/pedidos/{pedido_id}",
            json={"status": "enviado"},
            headers=headers
        )
        assert put_resp.status_code == 200
        assert put_resp.json()["status"] == "enviado"

        # Excluir pedido
        del_resp = await ac.delete(f"/pedidos/{pedido_id}", headers=headers)
        assert del_resp.status_code == 204
