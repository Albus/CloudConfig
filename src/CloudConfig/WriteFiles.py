from pathlib import Path
from typing import Optional

from pydantic import constr

from lib import BaseModel, Type


class WriteFiles(BaseModel):
  path: Path = "/tmp"
  permissions: constr(regex="^[0-9]{4}$") = "0400"
  owner: Type.Users = Type.Users.root
  content: str = ""
  append: bool
  container: Optional[str]
