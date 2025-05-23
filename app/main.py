import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth, client, debug, product
from app.core.database import engine, Base
from fastapi.openapi.utils import get_openapi
import sentry_sdk

sentry_sdk.init(
    dsn="https://7a49cdf156639d9a84b49dcde1b7492e@o4509367948935168.ingest.us.sentry.io/4509367950311424", # noqa E501
    send_default_pii=True,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lu Estilo API",
    description="API para gerenciamento de clientes, produtos e pedidos da Lu Estilo", # noqa E501
    version="1.0.0"
)

os.makedirs("static/img", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(debug.router, tags=["Debug"])
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(client.router, prefix="/clients", tags=["Clientes"])
app.include_router(product.router, prefix="/products", tags=["Produtos"])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
