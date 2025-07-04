#backend/app/routes/tasks.py
from flask import Blueprint

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return "TODO: listar tareas"
