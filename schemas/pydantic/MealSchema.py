from pydantic import BaseModel


class AuthorPostRequestSchema(BaseModel):
    name: str


class MealSchema(AuthorPostRequestSchema):
    id: int
