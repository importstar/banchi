from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class BaseSchema(BaseModel):
    id: PydanticObjectId = Field(
        # default_factory=PydanticObjectId,
        # alias="_id",
        example="0",
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
