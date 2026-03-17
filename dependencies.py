from fastapi import Depends
from sqlalchemy.orm import Session
from shared.db import get_admin_db, get_registiration_db, get_aygit_db
from services.auth import AuthService
from services.registiration import RegistirationService
from services.contract_verification import ContractVerificationService
from services.resource import ResourceService
from services.package import PackageService
from services.company import CompanyService

def get_auth_service(db: Session = Depends(get_admin_db)) -> AuthService:
    return AuthService(db=db)

def get_registiration_service(db: Session = Depends(get_registiration_db)) -> RegistirationService:
    return RegistirationService(db=db)

def get_contract_verification_service(db: Session = Depends(get_registiration_db)) -> ContractVerificationService:
    return ContractVerificationService(db=db)

def get_resource_service(db: Session = Depends(get_aygit_db)) -> ResourceService:
    return ResourceService(db=db)

def get_package_service(db: Session = Depends(get_aygit_db)) -> PackageService:
    return PackageService(db=db)

def get_company_service(db: Session = Depends(get_aygit_db)) -> CompanyService:
    return CompanyService(db=db)