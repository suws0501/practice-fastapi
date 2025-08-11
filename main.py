from src.api.main_router import router as main_router
from fastapi import FastAPI, Request
import json
import sys
print(sys.path)

app = FastAPI()

# @app.middleware("http")
# async def log_requests(request: Request, call_next):
    
#     print(f"\n--- Incoming Request ---")
#     print(f"{request.method} {request.url}")
    
    
#     for name, value in request.headers.items():
#         print(f"{name}: {value}")
    
#     try:
#         body = await request.body()
#         if body:
#             try:
#                 print("Body JSON:", json.loads(body))
#             except json.JSONDecodeError:
#                 print("Body (raw):", body.decode())
#         else:
#             print("Body: <empty>")
#     except Exception as e:
#         print(f"Error reading body: {e}")


#     response = await call_next(request)
    
    
#     print(f"Response status: {response.status_code}")
#     print(f"--- End Request ---\n")
#     return response

app.include_router(main_router)