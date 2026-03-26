from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from shared.models.aygit_base import AygitBaseModel

class CompanyModel(AygitBaseModel):
    __tablename__ = "companies"

    logo = Column(String, nullable=True)      
    title = Column(String, nullable=False)
    tax_number = Column(String, nullable=False)
    tax_department = Column(String, nullable=True)    
    address = Column(String, nullable=False)
    district = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    fax = Column(String, nullable=True)
    mail = Column(String, nullable=True)
    web_site = Column(String, nullable=True)
    slug = Column(String, nullable=False, unique=True)    
    type = Column(String, nullable=False)
    is_accounting_firm = Column(Boolean, nullable=True)
    
    # Yeni eklenen NES alanları
    first_name = Column(String(75), nullable=True)
    last_name = Column(String(75), nullable=True)
    einvoice_alias = Column(String(150), nullable=True)
    edespatch_alias = Column(String(150), nullable=True)
    is_export_company = Column(Boolean, default=False)

    nes_username = Column(String(100), nullable=True)
    nes_password = Column(String(100), nullable=True)
    environment = Column(String(20), nullable=True) # TEST, PRODUCTION
    app_key = Column(String(255), nullable=True)
    app_secret = Column(String(255), nullable=True)
    is_esmm_user = Column(Boolean, default=False)
    is_emm_user = Column(Boolean, default=False)
    xslt_template_name = Column(String(100), nullable=True)
    default_series = Column(String(3), nullable=True)

    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    currency = relationship("CurrencyModel", lazy="select")

    sector_id = Column(Integer, ForeignKey("sectors.id"), nullable=True)
    sector = relationship("SectorModel", lazy="select")

    accounting_company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    accounting_company = relationship("CompanyModel", foreign_keys=[accounting_company_id], uselist=False, lazy="select")

    package_id = Column(Integer, ForeignKey("packages.id"), nullable=True)
    package = relationship("PackageModel", lazy="select")

    package_expires_at = Column(DateTime, nullable=True)


    def to_dict(self):
        return {
            "id": self.id,
            "logo": self.logo if self.logo else None,
            "title": self.title,            
            "tax_number": self.tax_number,
            "tax_department": self.tax_department,            
            "address": self.address,
            "district": self.district,
            "city":self.city,
            "country": self.country,
            "name": self.name,
            "surname": self.surname,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "fax": self.fax,
            "mail": self.mail,
            "web_site": self.web_site,
            "slug": self.slug,
            "sector": self.sector.to_dict() if self.sector else None,
            "currency": self.currency.to_dict(),
            "type": self.type,
            "accounting_company": self.accounting_company.to_dict() if self.accounting_company else None,
            "nes_username": self.nes_username,
            "environment": self.environment,
            "is_esmm_user": self.is_esmm_user,
            "is_emm_user": self.is_emm_user,
            "xslt_template_name": self.xslt_template_name,
            "default_series": self.default_series,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "einvoice_alias": self.einvoice_alias,
            "edespatch_alias": self.edespatch_alias,
            "is_export_company": self.is_export_company,
            "package": self.package.to_dict() if self.package else None,
            "is_accounting_firm": self.is_accounting_firm
        }