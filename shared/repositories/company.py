from sqlalchemy import or_
from sqlalchemy.orm import Session
from shared.repositories.base import BaseRepository
from shared.models import CompanyModel
from shared.schemas import PaginationSchema
from typing import Optional, List


class CompanyRepository(BaseRepository[CompanyModel]):
    def __init__(self, db: Session):
        super().__init__(model=CompanyModel, db=db)

    def get(self, skip: int, limit: int, search: Optional[str]) -> PaginationSchema:
        query = self.db.query(self.model).filter(self.model.is_active == True)
        total_count = query.count()

        if search:
            query = query.filter(
                (self.model.full_name.ilike(f"%{search}%")) |
                (self.model.short_name.ilike(f"%{search}%")) |
                (self.model.tax_number.ilike(f"%{search}%")) |
                (self.model.slug.ilike(f"%{search}%"))
            )

        count = query.count()
        total_pages = (count + limit - 1) // limit if limit > 0 else 1
        current_page = (skip // limit) + 1 if limit > 0 else 1

        data = query.order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

        return PaginationSchema(
            total_count=total_count,
            count=count,
            skip=skip,
            limit=limit,
            current_page=current_page,
            total_pages=total_pages,
            data=data
        )
    
    def get_accounting_companies(self, search: Optional[str]) -> List[CompanyModel]:
        query = self.db.query(self.model).filter(self.model.is_active == True, self.model.is_accounting_firm == True)
        if search:
            query = query.filter(
                or_(
                    self.model.full_name.ilike(f"%{search}%"),
                    self.model.short_name.ilike(f"%{search}%")
                )
            )        
        data = query.all()
        return data