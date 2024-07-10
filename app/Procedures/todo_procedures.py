from flask_pymongo import PyMongo
from typing import List, Dict
from bson.objectid import ObjectId
from app.Models.todo_model import ToDoModel
from app.Database.db_config import get_database
from datetime import datetime


async def get_all_tasks() -> List[Dict]:
    mongo = get_database()
    cursor = mongo.tasks.find()
    tasks = []
    async for task in cursor:
        tasks.append(ToDoModel.from_mongo(task))
    return tasks

async def create_task(data: Dict) -> Dict:
    mongo = get_database()
    new_task = ToDoModel(title=data['title'], description=data.get('description', ''),
                         completed=data.get('completed', False))
    result = mongo.db.tasks.insert_one(new_task.dict())
    new_task.id = str(result.inserted_id)
    return new_task.dict()


async def update_task(task_id: str, data: Dict) -> Dict:
    mongo = get_database()
    updated_task = ToDoModel(**data, updated_at=datetime.now())
    mongo.db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": updated_task.dict()})
    return updated_task.dict()


async def delete_task(task_id: str) -> None:
    mongo = get_database()
    mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})
