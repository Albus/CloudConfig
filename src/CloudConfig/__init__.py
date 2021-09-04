from pathlib import WindowsPath
from typing import List, Optional

from CloudConfig.Rancher import Rancher
from CloudConfig.WriteFiles import WriteFiles
from CloudConfig.lib.base import BaseModel


class Config(BaseModel):
  class Config(BaseModel.Config):
    json_encoders = {
      WindowsPath: lambda v: v.as_posix(),
    }

  hostname: Optional[str]
  rancher: Optional[Rancher] = Rancher()
  ssh_authorized_keys: Optional[List[str]]
  write_files: Optional[List[WriteFiles]]
