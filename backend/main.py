"""
Main FastAPI application.
This file contains all API routes for the Task Manager.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="REST API for managing personal tasks and goals.",
    version="1.0.0"
)

@app.get("/", tags=["Home"])
def home():
    return {"message": "Welcome to Task Manager API"}

@app.post("/tasks", tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):

    new_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "Task Manager API"
    }

# ==========================
# GET ALL TASKS
# ==========================

@app.get("/tasks", tags=["Tasks"])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks


# ==========================
# GET TASK BY ID
# ==========================

@app.get("/tasks/{task_id}", tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# ==========================
# UPDATE TASK
# ==========================

@app.put("/tasks/{task_id}", tags=["Tasks"])
def update_task(task_id: int, updated_task: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed

    db.commit()
    db.refresh(task)

    return task


# ==========================
# DELETE TASK
# ==========================

@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}