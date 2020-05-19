from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: str = "200"
    msg: str = "success"
    data: dict