# backend/app/models/task.py

# Datos en memoria
_tasks = []
_next_id = 1

def get_all(priority=None):
    """
    Devuelve la lista de tareas.
    Si se pasa priority ('alta', 'media', 'baja'), filtra por prioridad.
    """
    if priority:
        return [t for t in _tasks if t['priority'] == priority]
    return list(_tasks)

def get_by_id(task_id):
    """Retorna la tarea con el id dado o None si no existe."""
    return next((t for t in _tasks if t['id'] == task_id), None)

def create(title, priority):
    """Crea una nueva tarea, le asigna un id único y la devuelve."""
    global _next_id
    task = {
        'id': _next_id,
        'title': title,
        'priority': priority
    }
    _tasks.append(task)
    _next_id += 1
    return task

def delete(task_id):
    """Elimina la tarea con el id dado. Devuelve True si la eliminó, False si no la encontró."""
    global _tasks
    before = len(_tasks)
    _tasks = [t for t in _tasks if t['id'] != task_id]
    return len(_tasks) < before

def update(task_id, title=None, priority=None):
    """
    Actualiza título y/o prioridad de la tarea dada.
    Devuelve la tarea modificada o None si no existe.
    """
    task = get_by_id(task_id)
    if not task:
        return None
    if title is not None:
        task['title'] = title
    if priority is not None:
        task['priority'] = priority
    return task
