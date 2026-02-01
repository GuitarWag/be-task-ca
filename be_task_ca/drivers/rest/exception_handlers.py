from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from be_task_ca.use_cases.exceptions.user_exceptions import (
    UserNotFoundError,
    EmailAlreadyExistsError,
)
from be_task_ca.use_cases.exceptions.item_exceptions import (
    ItemNotFoundError,
    ItemAlreadyExistsError,
    InsufficientStockError,
)
from be_task_ca.use_cases.exceptions.cart_exceptions import ItemAlreadyInCartError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(
        request: Request, exc: UserNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "user_not_found", "message": str(exc)},
        )

    @app.exception_handler(EmailAlreadyExistsError)
    async def email_exists_handler(
        request: Request, exc: EmailAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "email_already_exists", "message": str(exc)},
        )

    @app.exception_handler(ItemNotFoundError)
    async def item_not_found_handler(
        request: Request, exc: ItemNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "item_not_found", "message": str(exc)},
        )

    @app.exception_handler(ItemAlreadyExistsError)
    async def item_exists_handler(
        request: Request, exc: ItemAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "item_already_exists", "message": str(exc)},
        )

    @app.exception_handler(InsufficientStockError)
    async def insufficient_stock_handler(
        request: Request, exc: InsufficientStockError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "insufficient_stock", "message": str(exc)},
        )

    @app.exception_handler(ItemAlreadyInCartError)
    async def item_in_cart_handler(
        request: Request, exc: ItemAlreadyInCartError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "item_already_in_cart", "message": str(exc)},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "validation_error", "message": str(exc)},
        )
