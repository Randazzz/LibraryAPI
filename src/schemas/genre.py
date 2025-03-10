from pydantic import BaseModel, ConfigDict, Field


class GenreCreate(BaseModel):
    name: str = Field(..., max_length=16)


class GenreResponse(GenreCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
