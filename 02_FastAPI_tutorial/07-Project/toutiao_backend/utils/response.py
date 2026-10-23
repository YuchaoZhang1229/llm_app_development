from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.users import UserAuthResponse, UserInfoResponse


def success_response(message: str = "success", data: UserAuthResponse| UserInfoResponse | None = None):
    content = {"code": 200, "message": message, "data": data}
    return JSONResponse(content=jsonable_encoder(content))


if __name__ == "__main__":
    res = success_response()
    print(res.body)