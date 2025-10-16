import json

from aiohttp import web
from pydantic import BaseModel, ValidationError, field_validator


class BaseOwnerReq(BaseModel):
    header: str
    description: str
    owner: str

    @field_validator("owner")
    @classmethod
    def check_owner(cls, v: str):
        if len(v) <= 1:
            raise ValueError("owner must be at 1 letter long")
        return v


class CreateOwnerRequest(BaseOwnerReq):
    pass


class UpdateOwnerRequest(BaseOwnerReq):
    pass


def validate(schema: type[CreateOwnerRequest | UpdateOwnerRequest], json_data: dict):
    try:
        schema_inst = schema(**json_data)
        return schema_inst.model_dump()
    except ValidationError as e:
        errors = e.errors()
        for error in errors:
            error.pop("ctx", None)
        raise web.HTTPBadRequest(
            text=json.dumps({"errors": errors}), content_type="application/json"
        )
