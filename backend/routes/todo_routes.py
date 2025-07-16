from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import select
from models.todo_model import todo, todoDTO, priority, todostatus
from database.DB import Session, get_session
from utils.jwtdependencies import JWTBearer

TodoRoutes = APIRouter(dependencies=[Depends(JWTBearer)])


# Create todo
@TodoRoutes.post("/todo/", status_code=status.HTTP_201_CREATED)
def create_todo(todo_data: todo, session: Session = Depends(get_session)):
    session.add(todo_data)
    session.commit()
    session.refresh(todo_data)
    return todoDTO(
        task=todo_data.task,
        taskdescription=todo_data.taskdescription,
        taskid=todo_data.taskid,
        taskpriority=priority(todo_data.taskpriority).name,
        taskstatus=todostatus(todo_data.taskstatus).name,
    )


# Get all todos
@TodoRoutes.get("/getalltodo/")
def get_all_todo(session: Session = Depends(get_session)):
    todos = session.exec(select(todo)).all()
    if not todos:
        raise HTTPException(status_code=404, detail="No todos found")
    return [
        todoDTO(
            task=to.task,
            taskdescription=to.taskdescription,
            taskid=to.taskid,
            taskpriority=priority(to.taskpriority).name,
            taskstatus=todostatus(to.taskstatus).name,
        )
        for to in todos
    ]


# Get single Todo
@TodoRoutes.get("/getatodo/{todo_id}")
def get_todo(todo_id: int, session: Session = Depends(get_session)):
    Todo = session.get(todo, todo_id)
    if not Todo:
        raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found")
    return Todo


# Update Todo
@TodoRoutes.put("/updatetodo/{todo_id}")
def update_todo(todo_id: int, updates: todo, session: Session = Depends(get_session)):
    Todo = session.get_one(todo, todo_id)
    if not Todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )
    for key, value in updates.model_dump().items():
        setattr(Todo, key, value)

    session.commit()
    session.refresh(Todo)
    return Todo


# Delete Todo
@TodoRoutes.delete("/deletetodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(todo_id: int, session: Session = Depends(get_session)):
    Todo = session.get(todo, todo_id)
    if not Todo:
        raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found")

    session.delete(Todo)
    session.commit()
    return None
