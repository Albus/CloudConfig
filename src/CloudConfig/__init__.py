from abc import ABC
from enum import Enum
from ipaddress import IPv4Address, IPv4Interface
from pathlib import Path, WindowsPath
from typing import List, Union, Optional, Dict

import orjson
from pydantic import BaseModel as PydanticBaseModel, StrictStr, Field, constr, PositiveInt, validator


class BaseModel(PydanticBaseModel, ABC):
    class Config:
        validate_all = True
        validate_assignment = True
        anystr_strip_whitespace = True
        arbitrary_types_allowed = True
        copy_on_model_validation = False


class BaseModelWithRoot(BaseModel, ABC):

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


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
            def validator_root(cls, v: StrictStr):
                return v.upper()

        class Device(BaseModel):
            __root__: constr(regex="^/dev/[a-z0-9]+$", to_lower=True, strict=True, strip_whitespace=True)


class CloudConfig(BaseModel):
    class Config:

        @staticmethod
        def _orjson_dumps(val, *, default) -> str:
            return orjson.dumps(val, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS, default=default).decode()

        json_dumps = _orjson_dumps

        json_encoders = {
            WindowsPath: lambda v: v.as_posix(),
        }

    class Rancher(BaseModel):
        class SSH(BaseModel):
            daemon: str = True
            port: PositiveInt = 22

        class State(BaseModel):
            autoformat: List[Type.Disk.Device] = []
            boot_dev: Type.Disk.Label = "LABEL=RANCHER_BOOT"
            boot_fstype: Type.FS = Type.FS.auto
            cryptsetup: bool = False
            dev: Type.Disk.Label = "LABEL=RANCHER_STATE"
            directory: str = ""
            fstype: Type.FS = Type.FS.auto
            lvm_scan: bool = False
            mdadm_scan: bool = False
            oem_dev: Type.Disk.Label = "LABEL=RANCHER_OEM"
            oem_fstype: Type.FS = Type.FS.auto
            required: bool = False
            rngd: bool = True
            script: str = ""
            wait: bool = True

        class ServicesInclude(BaseModel):
            hyperv_vm_tools: bool = Field(default=False, alias="hyperv-vm-tools")
            amazon_ecs_agent: bool = Field(default=False, alias="amazon-ecs-agent")
            container_cron: bool = Field(default=False, alias="container-cron")
            zfs: bool = Field(default=False, alias="zfs")
            kernel_extras: bool = Field(default=False, alias="kernel-extras")
            kernel_headers: bool = Field(default=False, alias="kernel-headers")
            kernel_headers_system_docker: bool = Field(default=False, alias="kernel-headers-system-docker")
            open_vm_tools: bool = Field(default=False, alias="open-vm-tools")
            qemu_guest_agent: bool = Field(default=False, alias="qemu-guest-agent")
            amazon_metadata: bool = Field(default=False, alias="amazon-metadata")
            volume_cifs: bool = Field(default=False, alias="volume-cifs")
            volume_efs: bool = Field(default=False, alias="volume-efs")
            volume_nfs: bool = Field(default=False, alias="volume-nfs")
            modem_manager: bool = Field(default=False, alias="modem-manager")
            waagent: bool = Field(default=False, alias="waagent")
            virtualbox_tools: bool = Field(default=False, alias="virtualbox-tools")
            docker_compose: bool = Field(default=False, alias="docker-compose")

        class Network(BaseModel):
            class DNS(BaseModel):
                nameservers: List[IPv4Address] = ["8.8.8.8", "8.8.4.4"]

            class Interfaces(BaseModelWithRoot):
                """
                https://burmillaos.org/docs/networking/#configuring-network-interfaces
                """

                class eth(BaseModel):
                    class Config:
                        arbitrary_types_allowed = True

                    dhcp: bool = True
                    address: Optional[IPv4Interface]

                class wlan(eth):
                    wifi_network: constr(min_length=1, strip_whitespace=True, strict=True)

                __root__: Dict[str, Union[wlan, eth]] = []

            class WifiNetworks(BaseModelWithRoot):
                class Network(BaseModel):
                    ssid: str
                    psk: str
                    scan_ssid: int = 1

                __root__: Dict[str, Network]

            dns = DNS()
            interfaces: Optional[Interfaces]
            wifi_networks: Optional[WifiNetworks]

        class Environment(BaseModel):
            TZ: str = r"Europe/Moscow"

        class Docker(BaseModel):
            engine: Optional[constr(regex=r"^docker-[0-9]+\.[0-9]+\.[0-9]+$")]

        services_include: ServicesInclude = ServicesInclude()
        network: Network = Network()
        environment: Environment = Environment()
        runcmd: List[Union[str, List[str]]] = []
        ssh: SSH = SSH()
        state: State = State()
        preload_wait: bool = True
        docker: Optional[Docker]

    class WriteFiles(BaseModel):
        path: Path = "/tmp"
        permissions: constr(regex="^[0-9]{4}$") = "0400"
        owner: Type.Users = Type.Users.root
        content: str = ""
        append: bool
        container: Optional[str]

    hostname: Optional[str]
    rancher: Rancher = Rancher()
    ssh_authorized_keys: List[StrictStr] = []
    write_files: Optional[List[WriteFiles]]
