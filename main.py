
from sqlmodel import Session, select
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Annotated

from database import create_db_and_tables
from depend import get_session
from models import TaskCreate, TaskResponse,  Tasks, TaskUpdate

# Plain API without Dependency injection

app : FastAPI = FastAPI()


@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Your Todo App is Running ;-)"}


@app.get("/tasks", response_model=list[TaskResponse] | None, tags=["Namaz"])
def get_tasks(session: Annotated[Session, Depends(get_session)]):
    tasks = session.exec(select(Tasks)).all()
    return tasks


@app.post("/tasks", response_model=TaskResponse, tags=["Namaz"])
def create_task(task: TaskCreate, session: Annotated[Session, Depends(get_session)]):
    task_to_add = Tasks(**task.model_dump(exclude_unset=True))
    session.add(task_to_add)
    session.commit()
    session.refresh(task_to_add)
    return task_to_add


@app.get("/tasks/{task_title}", response_model=TaskResponse, tags=["Namaz"]) 
def get_single_task(task_title: str, session: Annotated[Session, Depends(get_session)]):
    task = session.exec(select(Tasks).where(Tasks.title == task_title)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_title}", tags=["Namaz"])
def update_task(task_title: str, task_data: TaskUpdate, session: Annotated[Session, Depends(get_session)]):
    task = session.exec(select(Tasks).where(Tasks.title == task_title)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    print("Hero in DB:", task)
    print("Hero Data from client:", task_data)
    
    hero_dict_data = task_data.model_dump(exclude_unset= True)
    print("Hero Dict Data:", hero_dict_data)
    
    for key, value in hero_dict_data.items():
        setattr(task, key, value)
    print("Hero after update:", task)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


@app.delete("/tasks/{task_title}", tags=["Namaz"])
def delete_task(task_title: str, session: Annotated[Session, Depends(get_session)]):
    task = session.exec(select(Tasks).where(Tasks.title == task_title)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}
