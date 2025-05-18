import secrets
import warnings
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated, Any, Literal
from pydantic import AnyUrl, BeforeValidator, MySQLDsn,  computed_field
from pydantic_core import MultiHostUrl

print("Current working dir:", os.getcwd())

def parse_cors(v: Any):
  if isinstance(v,str) and not v.startswith("["):
    return [i.strip() for i in v.split(",")]
  elif isinstance(v, list | str):
        return v
  raise ValueError(v)

class Settings(BaseSettings):
  model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )
  
  PREFIX_ROUTER: str = "/api/v1"

  SECRET_KEY: str = secrets.token_urlsafe(32)
  # 60 minutes * 24 hours * 8 days = 8 days
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
  FRONTEND_HOST: str = "http://localhost:5173"
  ENVIRONMENT: Literal["local", "staging", "production"] = "local"

  BACKEND_CORS_ORIGINS: Annotated[
    list[AnyUrl] | str,  BeforeValidator(parse_cors)
  ] = []

  @computed_field  # type: ignore[prop-decorator]
  @property
  def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]
  
  PROJECT_NAME: str
  MYSQL_SERVER: str
  MYSQL_PORT: int = 3306
  MYSQL_USER: str
  MYSQL_PASSWORD: str = ""
  MYSQL_DB: str = ""

  def SQLMODEL_DATABASE_URI(self) -> MySQLDsn: 
    return MultiHostUrl.build(
      scheme="mysql+mysqlconnector",
      username=self.MYSQL_USER,
      password=self.MYSQL_PASSWORD,
      host=self.MYSQL_SERVER,
      port=self.MYSQL_PORT,
      path=self.MYSQL_DB,

    )


settings = Settings()
