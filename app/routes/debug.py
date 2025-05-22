import os
from fastapi import APIRouter

router = APIRouter()

if os.getenv("environment", "development") == "development":
    @router.get("/sentry-debug")
    async def trigger_error():
        return 1 / 0
