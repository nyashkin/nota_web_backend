from pydantic import BaseModel


class BaseAppSchema(BaseModel):
    class Config:
        from_attributes = True
