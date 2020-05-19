from pydantic import BaseModel


class UserCreateResponse(BaseModel):
    code: str = None
    # data: dict = {"token": str}
    data: dict
    msg: str = None
