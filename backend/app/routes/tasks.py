# backend/app/routes/tasks.py
import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.task import Task
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['GET'])
def list_tasks():
    """
    GET /api/tasks
    Parámetros opcionales:
      - priority: 'alta' | 'media' | 'baja'
    Devuelve lista de tareas, filtradas si se indicó priority,
    ordenadas por created_at descendente.
    """
    priority = request.args.get('priority', type=str)
    query = Task.query
    if priority in ('alta', 'media', 'baja'):
        query = query.filter_by(priority=priority)
    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200

@tasks_bp.route('', methods=['POST'])
def add_task():
    """
    POST /api/tasks
    Recibe JSON { title, priority }.
    Valida título no vacío y prioridad válida.
    Crea y devuelve la tarea con estado 201.
    """
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    priority = (data.get('priority') or '').strip()

    # Validaciones
    if not title:
        return jsonify({'error': 'El título es obligatorio'}), 400
    if priority not in ('baja', 'media', 'alta'):
        return jsonify({'error': 'Prioridad inválida'}), 400

    task = Task(title=title, priority=priority)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    PUT /api/tasks/<task_id>
    Recibe JSON { title, priority }.
    Valida datos, actualiza la tarea y devuelve el objeto.
    """
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    priority = (data.get('priority') or '').strip()

    if not title:
        return jsonify({'error': 'El título es obligatorio'}), 400
    if priority not in ('baja', 'media', 'alta'):
        return jsonify({'error': 'Prioridad inválida'}), 400

    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    task.title = title
    task.priority = priority
    db.session.commit()
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    DELETE /api/tasks/<task_id>
    Elimina la tarea indicada y devuelve mensaje de confirmación.
    """
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tarea eliminada'}), 200
