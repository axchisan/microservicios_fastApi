from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo para las tareas
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

# Base de datos simulada (lista en memoria)
tasks = []


# Endpoint para crear una tarea
@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="Task ID already exists")
    tasks.append(task)
    return task


# Endpoint para listar todas las tareas
@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return tasks



# Endpoint para obtener una tarea por ID
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")



# Endpoint para actualizar una tarea
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")


# Endpoint para eliminar una tarea
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")