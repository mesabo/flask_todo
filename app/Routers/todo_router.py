from flask import Blueprint, request, jsonify
from app.Procedures.todo_procedures import get_all_tasks, create_task, update_task, delete_task

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = get_all_tasks()
    return jsonify(tasks), 200


@todo_bp.route('/tasks', methods=['POST'])
def create_task_route():
    data = request.json
    new_task = create_task(data)
    return jsonify(new_task), 201


@todo_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task_route(task_id):
    data = request.json
    updated_task = update_task(task_id, data)
    return jsonify(updated_task), 200


@todo_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    delete_task(task_id)
    return '', 204
