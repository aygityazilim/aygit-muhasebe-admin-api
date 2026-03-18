from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from shared.db import AdminBase, admin_engine
from shared.utils import http_exception_handler, request_validation_exception_handler, internal_server_exception_handler
from routers.auth import router as auth_router
from routers.registiration import router as registiration_router
from routers.contract_verification import router as contract_verification_router
from routers.resource import router as resource_router
from routers.package import router as package_router
from routers.company import router as company_router
from routers.ticket import router as ticket_router

AdminBase.metadata.create_all(bind=admin_engine)

app = FastAPI(
    root_path="/admin",
    title="Admin Service",
    description="Admin Service",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, internal_server_exception_handler)


app.include_router(auth_router)
app.include_router(registiration_router)
app.include_router(contract_verification_router)
app.include_router(resource_router)
app.include_router(package_router)
app.include_router(company_router)
app.include_router(ticket_router)