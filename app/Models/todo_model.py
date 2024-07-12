from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import Optional

class ToDoModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    title: str
    description: Optional[str] = ""
    completed: Optional[bool] = False
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            ObjectId: lambda oid: str(oid),
            datetime: lambda dt: dt.isoformat() if dt else None,
        }

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        result.pop("_id", None)  # Remove _id field for serialization
        return result

    @classmethod
    def from_mongo(cls, data: dict):
        if "_id" in data:
            data["id"] = str(data.pop("_id"))
        return cls(**data)
