from pathlib import WindowsPath
from typing import List, Optional

from CloudConfig.Rancher import Rancher
from CloudConfig.WriteFiles import WriteFiles
from lib import BaseModel, BaseConfig


class Config(BaseModel):
  class Config(BaseConfig):
    json_encoders = {
      WindowsPath: lambda v: v.as_posix(),
    }

  hostname: Optional[str]
  rancher: Optional[Rancher] = Rancher()
  ssh_authorized_keys: Optional[List[str]]
  write_files: Optional[List[WriteFiles]]
