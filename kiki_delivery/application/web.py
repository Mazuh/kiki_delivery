from traceback import print_exception
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from kiki_delivery.domain.shared.exceptions import DomainValidatorException

from .restful import customers_controller

app = FastAPI(debug=True)

app.include_router(customers_controller.router)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except DomainValidatorException as exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(message=str(exception)),
        )
    except Exception as exception:
        print_exception(exception)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=dict(message="Unknown error."),
        )


app.middleware("http")(catch_exceptions_middleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}
