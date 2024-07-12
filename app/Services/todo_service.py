from typing import List, Dict
from bson.objectid import ObjectId
from datetime import datetime
from app.Models.todo_model import ToDoModel
from app.Procedures.todo_procedures import get_all_tasks as get_all_tasks_db, create_task as create_task_db, \
    update_task as update_task_db, delete_task as delete_task_db


def get_all_tasks() -> List[Dict]:
    tasks = get_all_tasks_db()
    return tasks


def create_task(data: Dict) -> Dict:
    new_task = create_task_db(data)
    return new_task


def update_task(task_id: str, data: Dict) -> Dict:
    updated_task = update_task_db(task_id, data)
    return updated_task


def delete_task(task_id: str) -> None:
    delete_task_db(task_id)
