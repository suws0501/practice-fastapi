from src.api.todo_router import router as todo_router
from fastapi import APIRouter

router = APIRouter()

#router.include_router(hello_world_router)
router.include_router(todo_router)