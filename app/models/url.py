from sqlmodel import SQLModel, Field

class Url(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_code: str
    url: str = Field(max_length=2048)