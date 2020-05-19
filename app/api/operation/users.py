import jwt
from fastapi.exceptions import HTTPException

from app.models.users import User
from settings import GET


async def query_and_create_user(auth_dict: dict):
    res = await User.filter(username=auth_dict.get("username")).limit(1).all()
    if res:
        return res
    else:
        return await User.create(**auth_dict)


async def get_user_by_username(username: str):
    return await User.filter(username=username).limit(1).all()


async def get_user_by_id(id: int):
    return await User.get(id=id)


async def get_user_info(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, GET.SECRET_KEY, algorithms=[GET.ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = await get_user_by_username(username=username)
    if not user:
        raise credentials_exception
    return user[0]
