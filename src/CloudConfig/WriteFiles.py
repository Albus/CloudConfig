from pathlib import Path
from typing import Optional

from pydantic import constr

from CloudConfig.lib.base import BaseModel
from CloudConfig.lib.types import Users


class WriteFiles(BaseModel):
  path: Path = "/tmp"
  permissions: constr(regex="^[0-9]{4}$") = "0400"
  owner: Users = Users.root
  content: str = ""
  append: bool
  container: Optional[str]
