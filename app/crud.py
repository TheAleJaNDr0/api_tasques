from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate


def get_tasks(db: Session):
    """
    Input:
        db: database session
    Output:
        List all tasks
    """
    tasks = db.query(Task).all()
    print("All Tasks:", tasks)
    return tasks



def create_tasks(db: Session, task: TaskCreate):
    """
    Input:
        db: database session
    Output:
        Return the new task
    """
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    print("Created Task:", new_task)
    return new_task


def update_tasks(db: Session, task_id: int, task_update: TaskUpdate):
    """
    Input:
        db: database session
    Output:
        Updated some task fields
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        print(f"Task with ID {task_id} not found.")
        return None
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    print("Updated Task:", task)
    return task



def delete_tasks(db: Session, task_id: int):
    """
    Input:
        db: database session
    Output:
        Return delete task
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        print(f"Task with ID {task_id} not found.")
        return None
    db.delete(task)
    db.commit()
    print("Deleted Task:", task)
    return task
