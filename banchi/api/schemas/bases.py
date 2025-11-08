from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class BaseSchema(BaseModel):
    id: PydanticObjectId = Field(
        alias="_id",
        serialization_alias="id",
        # default_factory=PydanticObjectId,
        example="0",
    )

    class Config:
        from_attributes = True
        populate_by_name = True


class BaseSchemaList(BaseModel):
    page: int = 1
    size_per_page: int = 50
    page_size: int = 1
