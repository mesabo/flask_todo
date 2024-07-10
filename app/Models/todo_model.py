from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime


class ToDoModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    title: str
    description: Optional[str] = ""
    completed: Optional[bool] = False
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
            datetime: lambda dt: dt.isoformat() if dt else None,
        }
        json_schema_extra = {
            "example": {
                "id": "609c9e45a669ca8d9a4a8a10",
                "title": "Complete project tasks",
                "description": "Finish all pending tasks for the project",
                "completed": False,
                "created_at": datetime.now().isoformat(),
                "updated_at": None,
                "deleted_at": None,
            }
        }

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        result.pop("_id", None)
        return result

    @classmethod
    def from_mongo(cls, data: dict):
        return cls(**data)
