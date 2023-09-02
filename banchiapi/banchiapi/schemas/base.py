from bson import ObjectId
from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic_core import CoreSchema


class PyObjectId(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, any]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(type="string")
        return json_schema


class BaseSchema(BaseModel):
    id: PyObjectId | None = Field(default_factory=PyObjectId, alias="_id", example="0")

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {ObjectId: str}


class BaseEmbeddedSchema(BaseModel):
    class Config:
        from_attributes = True
