from typing import Generic, Type, TypeVar, List
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_all(self) -> List[ModelType]:      
        return self.db.query(self.model).all()

    def get_by_id(self, id: int) -> ModelType:
        return self.db.query(self.model).get(id)

    def create(self, data: dict) -> ModelType:
        obj = self.model(**data)
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def update(self, db_obj: ModelType, data: dict) -> ModelType:
        for key, value in data.items():
            setattr(db_obj, key, value)
        setattr(db_obj, "is_active", True)
        self.db.flush()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> ModelType:
        obj = self.get_by_id(id)
        if obj:
            obj.is_active = False
            self.db.flush()
        return obj


    def get_by_field(self, field: str, value: str) -> ModelType | None:
        return self.db.query(self.model).filter(getattr(self.model, field) == value).first()
    

    def bulk_create(
        self,
        rows: List[dict],       
    ) -> None:                  
        self.db.bulk_insert_mappings(
                self.model,
                rows,                
            )       
        self.db.flush()