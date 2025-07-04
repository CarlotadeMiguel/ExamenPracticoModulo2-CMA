# backend/app/routes/tasks.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def list_tasks():
    priority = request.args.get('priority')
    q = Task.query
    if priority:
        q = q.filter_by(priority=priority)
    return jsonify([t.to_dict() for t in q.all()]), 200

@tasks_bp.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'error': 'El título es obligatorio'}), 400
    new_task = Task(title=title, priority=data.get('priority','baja'))
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tarea eliminada'}), 200

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    data = request.get_json() or {}
    if 'title' in data:
        task.title = data['title'].strip() or task.title
    if 'priority' in data:
        task.priority = data['priority']
    db.session.commit()
    return jsonify(task.to_dict()), 200
