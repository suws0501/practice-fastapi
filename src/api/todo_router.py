# src/api/todo_router.py
from typing import List
from starlette.requests import Request
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.schemas.todo import *
from src.utils.db_utils import create_database_session
from src.crud.todo_crud import (
    create_todo_crud,
    get_all_todos_crud,
    update_todo_crud,
    delete_todo_crud
)

router = APIRouter()

@router.post("/todos", response_model=TodoCreatedResponse)
async def create_todo(
    request: Request,
    todo: TodoCreate,
    db: AsyncSession = Depends(create_database_session)
):
    client_ip = request.client.host
    print(f"Request from {client_ip} creating a new todo")
    return await create_todo_crud(db, todo)


@router.get("/todos", response_model=List[TodoResponse])
async def get_all_todos(db: AsyncSession = Depends(create_database_session)):
    return await get_all_todos_crud(db)


@router.put("/todos/{todo_id}", response_model=TodoUpdatedResponse)
async def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    db: AsyncSession = Depends(create_database_session)
):
    return await update_todo_crud(db, todo_id, todo_update)


@router.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: UUID,
    db: AsyncSession = Depends(create_database_session)
):
    await delete_todo_crud(db, todo_id)
    return {"message": "Todo deleted successfully"}
