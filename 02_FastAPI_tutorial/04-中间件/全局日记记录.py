import logging
import uuid
from fastapi import FastAPI, Request
app = FastAPI()

logger = logging.getLogger(__name__)

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    logger.error(f"【INFO】[{request_id}] {request.method} {request.url.path}")

    response = await call_next(request)

    logger.error(f"【INFO】[{request_id}] 响应 {response.status_code}")
    return response

@app.get("/")
async def logging():
    return {"Hello World1"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("全局日记记录:app", host="127.0.0.1", port=8000, reload=True)