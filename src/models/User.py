from uuid import UUID
from sqlmodel import SQLModel, Field

class User(SQLModel):
  uid: UUID = Field(default=None, primary_key=True)
  name: str
  email: str
  is_active: bool = True
