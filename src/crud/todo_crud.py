# src/crud/todo_crud.py
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.models.todo import Todo
from src.schemas.todo import TodoCreate, TodoUpdate


async def create_todo_crud(db: AsyncSession, todo: TodoCreate) -> Todo:
    new_todo = Todo(
        title=todo.title,
        completed=todo.completed,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    return new_todo


async def get_all_todos_crud(db: AsyncSession) -> list[Todo]:
    result = await db.execute(select(Todo))
    return result.scalars().all()


async def update_todo_crud(db: AsyncSession, todo_id: UUID, todo_update: TodoUpdate) -> Todo:
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


async def delete_todo_crud(db: AsyncSession, todo_id: UUID) -> None:
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    existing_todo = result.scalar_one_or_none()

    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    await db.delete(existing_todo)
    await db.commit()
