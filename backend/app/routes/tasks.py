#backend/app/routes/tasks.py
from flask import request, jsonify
from app.models.task import get_all, create, delete

@tasks_bp.route('/tasks', methods=['GET'])
def list_tasks():
    pr = request.args.get('priority')
    return jsonify(get_all(pr)),200

@tasks_bp.route('/tasks', methods=['POST'])
def add_task():
    d=request.get_json() or {}
    title=(d.get('title') or '').strip()
    if not title: return jsonify({'error':'El título es obligatorio'}),400
    return jsonify(create(title,d.get('priority','baja'))),201

@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
def del_task(id):
    if delete(id): return jsonify({'message':'Tarea eliminada'}),200
    return jsonify({'error':'Tarea no encontrada'}),404
