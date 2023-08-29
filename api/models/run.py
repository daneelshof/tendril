from pydantic import BaseModel

class Run(BaseModel):
    id: int | None = None
    name: str
    status: str | None = None
    result: str | None = None
