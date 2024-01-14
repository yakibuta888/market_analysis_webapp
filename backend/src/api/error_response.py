from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error_type: str
    message: str
    detail: str | None = None
