"""
API Key 认证：如果项目只是内部服务间调用，API Key 就够用了
"""
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

app = FastAPI()

API_KEY = "1234567890"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# 注意这里用了 Security 而非 Depends——功能上几乎一样，但 Security 会让 FastAPI 在 Swagger 文档中正确展示安全方案。
async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/protected/", dependencies=[Depends(get_api_key)])
async def protected_route():
    return {"message": "This is a protected route"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_key认证:app", host="127.0.0.1", port=8000, reload=True)


# http://127.0.0.1:8000/protected
# 需要添加请求头头 Header = {"X-API-Key": "1234567890"}