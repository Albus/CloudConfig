from abc import ABC
from enum import Enum

from pydantic import BaseModel as PydanticBaseModel, BaseConfig as PydanticBaseConfig, BaseModel, constr, validator


class Type:
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


class BaseModel(PydanticBaseModel, ABC):
  class Config:
    validate_all = True
    validate_assignment = True
    anystr_strip_whitespace = True
    arbitrary_types_allowed = False
    copy_on_model_validation = False


class BaseConfig(PydanticBaseConfig, ABC):

  @staticmethod
  def _orjson_dumps(val, *, default) -> str:
    from orjson.orjson import dumps, OPT_INDENT_2, OPT_SORT_KEYS
    return dumps(val, option=OPT_INDENT_2 | OPT_SORT_KEYS, default=default).decode()

  json_dumps = _orjson_dumps


class BaseModelWithRoot(BaseModel, ABC):

  def __iter__(self):
    return iter(self.__root__)

  def __getitem__(self, item):
    return self.__root__[item]
