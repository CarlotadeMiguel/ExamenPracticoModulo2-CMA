# backend/app/routes/tasks.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task

# Todas las rutas bajo /api/tasks
tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks_bp.route('', methods=['GET'])
def list_tasks():
    """
    GET /api/tasks?priority=alta|media|baja
    Devuelve la lista de tareas (filtrada opcionalmente).
    """
    priority = request.args.get('priority')
    q = Task.query
    if priority:
        q = q.filter_by(priority=priority)
    tasks = q.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200

@tasks_bp.route('', methods=['POST'])
def add_task():
    """
    POST /api/tasks
    Body JSON: { "title": "...", "priority": "baja" }
    """
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'error': 'El título es obligatorio'}), 400

    task = Task(title=title, priority=data.get('priority', 'baja'))
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    DELETE /api/tasks/<task_id>
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tarea eliminada'}), 200

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    PUT /api/tasks/<task_id>
    Body JSON: { "title": "...", "priority": "alta" }
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    data = request.get_json() or {}
    if 'title' in data:
        new_title = data['title'].strip()
        if new_title:
            task.title = new_title
    if 'priority' in data:
        task.priority = data['priority']

    db.session.commit()
    return jsonify(task.to_dict()), 200
