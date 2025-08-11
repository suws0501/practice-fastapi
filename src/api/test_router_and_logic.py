from typing import List
from starlette.requests import Request
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from uuid import UUID
from src.models.todo import Todo
from src.schemas.todo import *
from src.utils.db_utils import create_database_session
from datetime import datetime, timezone

router = APIRouter()

@router.post("/todos", response_model=TodoCreatedResponse)
async def create_todo(
    request: Request,
    todo: TodoCreate,
    db: AsyncSession = Depends(create_database_session)
):
    
    client_ip = request.client.host
    print(f"Request from {client_ip} creating a new todo")

    new_todo = Todo(
        title=todo.title,
        completed=todo.completed,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    #print(type(new_todo.id), repr(new_todo.id))


    return new_todo

@router.get("/todos", response_model=List[TodoResponse])
async def get_all_todos(db: AsyncSession = Depends(create_database_session)):
    result = await db.execute(select(Todo))
    todos = result.scalars().all()
    return todos

@router.put("/todos/{todo_id}", response_model=TodoUpdatedResponse)
async def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    db: AsyncSession = Depends(create_database_session)
):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    existing_todo = result.scalar_one_or_none()

    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_todo, field, value)

    await db.commit()
    await db.refresh(existing_todo)

    return existing_todo

@router.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: UUID,
    db: AsyncSession = Depends(create_database_session)
):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    existing_todo = result.scalar_one_or_none()

    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    await db.delete(existing_todo)
    await db.commit()

    return {"message": "Todo deleted successfully"}


