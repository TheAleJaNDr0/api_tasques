from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.orm import sessionmaker
from app.models import Base, Task
from app.schemas import TaskCreate, TaskUpdate
from app.crud import get_tasks, create_tasks, update_tasks, delete_tasks
from sqlalchemy import create_engine
import pytest

client = TestClient(app)

# TODO: els vostres test venen aqui

# Configurar base de datos en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Crea una sesión de prueba y la elimina al finalizar."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_task():
    response = client.post("/tasks/", json={"title": "Test Task", "description": "This is a test task", "completed": False})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["completed"] is False

def test_get_tasks():
    # Crear una tarea
    client.post("/tasks/", json={"title": "Test Task", "description": "This is a test task", "completed": False})
    # Obtener todas las tareas
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_task():
    response = client.post("/tasks/", json={"title": "Old Title", "description": "Old Description", "completed": False})
    task_id = response.json()["id"]
    update_response = client.put(f"/tasks/{task_id}", json={"title": "New Title"})
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["title"] == "New Title"

def test_delete_task():
    response = client.post("/tasks/", json={"title": "To Delete", "description": "Will be deleted", "completed": False})
    task_id = response.json()["id"]
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert client.get(f"/tasks/{task_id}").status_code == 404
