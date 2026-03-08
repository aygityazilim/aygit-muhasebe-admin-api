from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from shared.db import AdminBase, admin_engine
from shared.utils import http_exception_handler, request_validation_exception_handler, internal_server_exception_handler
from routers.auth import router as auth_router

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
