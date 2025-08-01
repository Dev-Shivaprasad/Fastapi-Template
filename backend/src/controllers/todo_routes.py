from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlmodel import select
from src.models.todo_model import todo, todoDTO, priority, todostatus
from core.database.DB import Session, get_session
from services.jwtdependencies import JWTBearer
from core.ratelimiter.customratelimiter import init_rate_limiter, burst_proof_ratelimit
from core.cache.rediscache import (
    get_cache,
    invalidate_cache,
    add_or_update_cache,
)

TodoRoutes = APIRouter(dependencies=[Depends(JWTBearer)], prefix="/todo")
ratelimiter = init_rate_limiter()


# Create todo
@TodoRoutes.post("/addtodo/", status_code=status.HTTP_201_CREATED)
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
    await add_or_update_cache(
        request.app,
        f"todo:{todo_data.taskid}",
        dto.model_dump(),
        otherkeytoupdate="getalltodo",
    )
    # Assuming you use list for todos
    # Optionally cache by ID too
    # redis_client.set(f"todo:{dto.taskid}", orjson.dumps(dto.model_dump()))

    return dto


# Get all todos
@TodoRoutes.get("/getalltodo/")
@burst_proof_ratelimit(ratelimiter, "2/second")
async def get_all_todo(request: Request, session: Session = Depends(get_session)):
    cache_key = "getalltodo"
    cached = await get_cache(request.app, cache_key)
    if cached is not None:
        # Convert back to list of todoDTOs
        todos_data = cached
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

    await add_or_update_cache(request.app, cache_key, returnabletodos)
    return returnabletodos


# Get single Todo
@TodoRoutes.get("/getatodo/{todo_id}")
@ratelimiter.limit("1/second", per_method=True)
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
    await add_or_update_cache(request.app, cache_key, Todo.model_dump())
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
    await add_or_update_cache(
        request.app,
        f"todo:{todo_id}",
        updates.model_dump(),
        otherkeytoupdate="getalltodo",
    )

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
    await invalidate_cache(request.app, "getalltodo")
    return None
