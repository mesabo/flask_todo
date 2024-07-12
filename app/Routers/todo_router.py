from flask import Flask, Blueprint, request, jsonify
from app.Services.todo_service import get_all_tasks, create_task, update_task, delete_task

app = Flask(__name__)

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = get_all_tasks()
    return tasks, 200


@todo_bp.route('/tasks', methods=['POST'])
def create_task_route():
    data = request.json
    new_task = create_task(data)
    print(new_task)
    return jsonify({
  "_id": {
    "$oid": "668ed63147fe51244e21e182"
  },
  "id": "609c9e45a669ca8d9a4a8a10",
  "title": "Complete project tasks",
  "description": "Finish all pending tasks for the project",
  "completed": False,
  "created_at": "2024-07-11T12:34:56",
  "updated_at": "",
  "deleted_at": ""
}), 201


@todo_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task_route(task_id):
    data = request.json
    updated_task = update_task(task_id, data)
    return jsonify(updated_task), 200


@todo_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    delete_task(task_id)
    return '', 204


# Register Blueprint
app.register_blueprint(todo_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
