from fastapi import APIRouter, Body
from fastapi.exceptions import HTTPException
from app.response.users import UserCreateResponse
from app.api.operation.users import query_and_create_user
from app.utils.authenticate import authenticate_user, create_access_token

app = APIRouter()


@app.post("/login/", response_model=UserCreateResponse, tags=['Users'])
async def user_login(*, username: str = Body(...), password: str = Body(...)):
    result_auth = authenticate_user(username, password)
    if not result_auth[0]:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await query_and_create_user(result_auth[-1])
    access_token = create_access_token(
        data={"email": result_auth[-1].get("email"), "username": result_auth[-1].get("username")})
    return {"code": 200, "msg": "success", "data": {"token": access_token}}
