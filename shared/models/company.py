from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from shared.models.aygit_base import AygitBaseModel

class CompanyModel(AygitBaseModel):
    __tablename__ = "companies"

    logo = Column(String, nullable=True) 
    full_name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    tax_number = Column(String, nullable=False)
    tax_department = Column(String, nullable=False)    
    address = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    mersis_number = Column(String, nullable=True)
    type = Column(String, nullable=False)
    is_accounting_firm = Column(Boolean, nullable=True)

    nes_username = Column(String(100), nullable=True)
    nes_password = Column(String(100), nullable=True)
    environment = Column(String(20), nullable=True) # TEST, PRODUCTION
    app_key = Column(String(255), nullable=True)
    app_secret = Column(String(255), nullable=True)
    is_esmm_user = Column(Boolean, default=False)
    is_emm_user = Column(Boolean, default=False)
    xslt_template_name = Column(String(100), nullable=True)
    default_series = Column(String(3), nullable=True)

    package_id = Column(Integer, ForeignKey("packages.id"), nullable=True)
    package = relationship("PackageModel", lazy="select")

    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    currency = relationship("CurrencyModel", lazy="select")

    package_expires_at = Column(DateTime, nullable=True)

    accounting_company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    accounting_company = relationship("CompanyModel", lazy="select")

    def to_dict(self):
        return {
            "id": self.id,
            "logo": self.logo if self.logo else None,
            "full_name": self.full_name,
            "short_name": self.short_name,
            "tax_number": self.tax_number,
            "tax_department": self.tax_department,            
            "address": self.address,
            "slug": self.slug,
            "sector": self.sector.to_dict() if self.sector else None,
            "mersis_number": self.mersis_number,
            "currency": self.currency.to_dict(),
            "type": self.type,
            "accounting_company": self.accounting_company.to_dict() if self.accounting_company else None,
            "nes_username": self.nes_username,
            "environment": self.environment,
            "is_esmm_user": self.is_esmm_user,
            "is_emm_user": self.is_emm_user,
            "xslt_template_name": self.xslt_template_name,
            "default_series": self.default_series,
            "package": self.package.to_dict()
        }