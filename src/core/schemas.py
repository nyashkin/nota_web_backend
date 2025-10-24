from pydantic import BaseModel
from pydantic import ConfigDict


class BaseAppSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
