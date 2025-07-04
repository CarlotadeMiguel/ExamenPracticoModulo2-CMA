# backend/tests/test_routes.py

import pytest
from app import create_app, db
from app.models.task import Task

@pytest.fixture
def app_client(tmp_path, monkeypatch):
    # Crea un app de prueba con base de datos en memoria
    test_app = create_app()
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    test_app.config['TESTING'] = True

    with test_app.app_context():
        db.create_all()
        yield test_app.test_client()
        db.drop_all()

def test_list_empty(app_client):
    resp = app_client.get('/api/tasks')
    assert resp.status_code == 200
    assert resp.get_json() == []

def test_create_and_list(app_client):
    # Crear tarea
    resp = app_client.post('/api/tasks', json={'title':'Prueba','priority':'alta'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['title'] == 'Prueba'
    assert data['priority'] == 'alta'
    # Listar tareas
    resp2 = app_client.get('/api/tasks')
    assert resp2.status_code == 200
    tasks = resp2.get_json()
    assert len(tasks) == 1
    assert tasks[0]['title'] == 'Prueba'

def test_delete(app_client):
    # Añade tarea
    resp = app_client.post('/api/tasks', json={'title':'Borrar','priority':'baja'})
    tid = resp.get_json()['id']
    # Borra tarea
    resp2 = app_client.delete(f'/api/tasks/{tid}')
    assert resp2.status_code == 200
    assert resp2.get_json()['message'] == 'Tarea eliminada'
    # Comprueba que ya no está
    resp3 = app_client.get('/api/tasks')
    assert resp3.get_json() == []

def test_update(app_client):
    # Añadir y actualizar
    resp = app_client.post('/api/tasks', json={'title':'Old','priority':'media'})
    tid = resp.get_json()['id']
    resp2 = app_client.put(f'/api/tasks/{tid}', json={'title':'New','priority':'alta'})
    assert resp2.status_code == 200
    updated = resp2.get_json()
    assert updated['title'] == 'New'
    assert updated['priority'] == 'alta'

def test_validation(app_client):
    # Título vacío
    resp = app_client.post('/api/tasks', json={'title':'   ','priority':'media'})
    assert resp.status_code == 400
    assert 'error' in resp.get_json()
