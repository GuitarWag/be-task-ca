from fastapi import FastAPI

from be_task_ca.drivers.rest.routers.user_router import router as user_router
from be_task_ca.drivers.rest.routers.item_router import router as item_router
from be_task_ca.drivers.rest.routers.cart_router import router as cart_router
from be_task_ca.drivers.rest.exception_handlers import register_exception_handlers

app = FastAPI(
    title="Shopping Cart API - Clean Architecture",
    description="",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

register_exception_handlers(app)

app.include_router(user_router)
app.include_router(item_router)
app.include_router(cart_router)


@app.get("/", tags=["health"])
async def root():
    return {
        "status": "healthy",
        "version": "2.0.0",
    }
