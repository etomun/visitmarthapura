import logging

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError

from src import account, visitor, address, event, queue
from src.account.dependencies import verify_token
from src.database import init_db
from src.exceptions import GeneralException

app = FastAPI()

#
# # Define OAuth2 scheme
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# # Configure OAuth2 in Swagger UI
# app.openapi_schema = {
#     "openapi": "3.0.0",
#     "info": {"title": "FastAPI", "version": "0.1.0"},
#     "security": [
#         {
#             "bearerAuth": []
#         }
#     ],
#     "components": {
#         "securitySchemes": {
#             "bearerAuth": {
#                 "type": "http",
#                 "scheme": "bearer",
#                 "bearerFormat": "JWT",
#             }
#         },
#     },
# }

# Initialize the database tables
init_db()


@app.exception_handler(GeneralException)
async def general_exception_handler(request, exc: GeneralException):
    logging.info(request)
    return exc.as_response()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    logging.info(request)
    general_exc = GeneralException(exc.status_code, exc.detail, exc.status_code, exc.detail)
    return general_exc.as_response()


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc: Exception):
    logging.info(request)
    status_500 = status.HTTP_500_INTERNAL_SERVER_ERROR
    message_500 = "Internal Server Error"
    if isinstance(exc, IntegrityError):
        general_exc = GeneralException(status_500, message_500, 12, str(exc))
    else:
        general_exc = GeneralException(status_500, message_500, 11, str(exc))
    return general_exc.as_response()


app.include_router(account.router, prefix="/api/auth", tags=["Account"])
app.include_router(event.router, prefix="/api/event", tags=["Event"])
app.include_router(queue.router, prefix="/api/queue", tags=["Event Visitor Queue"])
app.include_router(address.router, prefix="/api/address", tags=["Address"], dependencies=[Depends(verify_token)])
app.include_router(visitor.router, prefix="/api/visitor", tags=["Visitor"], dependencies=[Depends(verify_token)])


@app.get("/")
def read_root():
    return {"message": "Sugeng Rawuh"}