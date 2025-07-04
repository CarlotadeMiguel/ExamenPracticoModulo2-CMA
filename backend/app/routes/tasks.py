#backend/app/routes/tasks.py
from flask import request, jsonify
from app.models.task import tasks, next_id

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.get_json() or {}
    # validación mínima...
    new_task = {'id': next_id, 'title': data['title'], 'priority': data['priority']}
    tasks.append(new_task); next_id += 1
    return jsonify(new_task), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # eliminar lógica...
