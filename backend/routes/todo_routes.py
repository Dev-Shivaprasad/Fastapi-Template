from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlmodel import select
from models.todo_model import todo, todoDTO, priority, todostatus
from database.DB import Session, get_session
from utils.jwtdependencies import JWTBearer
import orjson
from database.cache.rediscache import (
    get_cache,
    invalidate_cache,
    addorupdate_cache,
)

TodoRoutes = APIRouter(dependencies=[Depends(JWTBearer)])


# Create todo
@TodoRoutes.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    request: Request, todo_data: todo, session: Session = Depends(get_session)
):
    # The below if statement shows error just ignore it
    if todo_data.taskpriority > 2 or todo_data.taskstatus > 2:  # type: ignore
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="taskpriority and taskstatus should be either : 0 = low | 1 : medium | 2 : High",
        )

    session.add(todo_data)
    session.commit()
    session.refresh(todo_data)

    dto = todoDTO(
        task=todo_data.task,
        taskdescription=todo_data.taskdescription,
        taskid=todo_data.taskid,
        taskpriority=priority(todo_data.taskpriority).name,
        taskstatus=todostatus(todo_data.taskstatus).name,
    )

    # Update Redis cache
    await addorupdate_cache(
        request.app,
        f"todos:{todo_data.taskid}",
        dto.model_dump(),
        otherkeytoupdate="getalltodo",
    )
    # Assuming you use list for todos
    # Optionally cache by ID too
    # redis_client.set(f"todo:{dto.taskid}", orjson.dumps(dto.model_dump()))

    return dto


# Get all todos
@TodoRoutes.get("/getalltodo/")
async def get_all_todo(request: Request, session: Session = Depends(get_session)):
    cache_key = "getalltodo"
    cached = await get_cache(request.app, cache_key)
    if cached:
        # Convert back to list of todoDTOs
        todos_data = orjson.loads(cached)
        return todos_data

    # DB fallback
    todos = session.exec(select(todo)).all()
    if not todos:
        raise HTTPException(status_code=404, detail="No todos found")

    returnabletodos = [
        todoDTO(
            task=to.task,
            taskdescription=to.taskdescription,
            taskid=to.taskid,
            taskpriority=priority(to.taskpriority).name,
            taskstatus=todostatus(to.taskstatus).name,
        ).model_dump()
        for to in todos
    ]

    await addorupdate_cache(
        request.app, cache_key, orjson.dumps(returnabletodos).decode()
    )
    return returnabletodos


# Get single Todo
@TodoRoutes.get("/getatodo/{todo_id}")
async def get_todo(
    todo_id: int, request: Request, session: Session = Depends(get_session)
):
    cache_key = f"todo:{todo_id}"
    cached_data = await get_cache(request.app, cache_key)

    if cached_data:
        return cached_data

    Todo = session.get(todo, todo_id)
    if not Todo:
        raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found")

    # Convert Enum values to string names
    todo_data = todoDTO(
        task=Todo.task,
        taskdescription=Todo.taskdescription,
        taskid=Todo.taskid,
        taskpriority=priority(Todo.taskpriority).name,
        taskstatus=todostatus(Todo.taskstatus).name,
    ).model_dump()

    await addorupdate_cache(request.app, cache_key, todo_data)
    return todo_data


# Update Todo
@TodoRoutes.put("/updatetodo/{todo_id}")
async def update_todo(
    todo_id: int,
    updates: todo,
    request: Request,
    session: Session = Depends(get_session),
):
    Todo = session.get(todo, todo_id)
    if not Todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    for key, value in updates.model_dump().items():
        setattr(Todo, key, value)

    session.commit()
    session.refresh(Todo)

    # Update cache
    await addorupdate_cache(request.app, str(todo_id), Todo)

    return Todo


# Delete Todo
@TodoRoutes.delete("/deletetodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(
    request: Request, todo_id: int, session: Session = Depends(get_session)
):
    Todo = session.get(todo, todo_id)
    if not Todo:
        raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found")

    session.delete(Todo)
    session.commit()
    await invalidate_cache(request.app, f"todo:{todo_id}")
    return None
