from enum import Enum

from pydantic import constr, validator

from CloudConfig.lib.base import BaseModel


class Users(str, Enum):
  root: str = "root"
  rancher: str = "rancher"


class FS(str, Enum):
  auto: str = "auto"
  ext4: str = "ext4"


class Disk:
  class Label(BaseModel):
    __root__: constr(regex="^LABEL=RANCHER_[A-Z0-9]+$", to_lower=False, strict=True, strip_whitespace=True)

    @validator("__root__", pre=True)
    def validator_root(cls, v: str):
      return v.upper()

  class Device(BaseModel):
    __root__: constr(regex="^/dev/[a-z0-9]+$", to_lower=True, strict=True, strip_whitespace=True)
