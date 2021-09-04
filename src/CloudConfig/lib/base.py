from abc import ABC

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel, ABC):
  class Config:
    @staticmethod
    def _orjson_dumps(val, *, default) -> str:
      from orjson.orjson import dumps, OPT_INDENT_2, OPT_SORT_KEYS
      return dumps(val, option=OPT_INDENT_2 | OPT_SORT_KEYS, default=default).decode()

    json_dumps = _orjson_dumps
    validate_all = True
    validate_assignment = True
    anystr_strip_whitespace = True
    arbitrary_types_allowed = False
    copy_on_model_validation = False


class BaseModelWithRoot(BaseModel, ABC):

  def __iter__(self):
    return iter(self.__root__)

  def __getitem__(self, item):
    return self.__root__[item]
