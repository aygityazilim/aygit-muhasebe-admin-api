from sqlalchemy.orm import Session
from shared.repositories import ResourceRepository
from shared.schemas import ListItemSchema


class ResourceService:
    def __init__(self, db: Session):
        self.db = db
        self.resource_repository = ResourceRepository(db=db)

    async def get_list(self) -> list[ListItemSchema]:
        items = self.resource_repository.get_all()
        return [
            ListItemSchema(
                id=item.id,
                name=item.key,
                description=item.path,
                metadata={
                    "sort_order": item.sort_order,
                    "is_menu": item.is_menu,
                    "parent_id": item.parent_id,
                }
            )
            for item in items
        ]
