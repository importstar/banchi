from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class BaseSchema(BaseModel):
    id: PydanticObjectId = Field(
        # default_factory=PydanticObjectId,
        # alias="_id",
        example="0",
    )

    class Config:
        from_attributes = True
        populate_by_name = True
        orm_mode = True
