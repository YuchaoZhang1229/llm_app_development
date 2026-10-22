from fastapi import FastAPI, Query,Depends
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

# 分页参数逻辑共用：商品列表和用户列表
def common_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=60)
) -> dict:
    return {"skip": skip, "limit": limit}

@app.get("/item/item_list")
def get_item_list(commons: dict = Depends(common_params)):
    return {"commons": commons}

@app.get("/user/user_list")
def get_user_list(commons: dict = Depends(common_params)):
    return {"commons": commons}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)  # 【重要】"main:app" 中的 main 必须与文件名 main.py 一致，否则启动失败