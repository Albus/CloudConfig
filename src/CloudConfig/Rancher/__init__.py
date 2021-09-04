from ipaddress import IPv4Address, IPv4Interface
from typing import Optional, List, Dict, Union

from pydantic import PositiveInt, Field, constr

from lib import BaseModel, Type, BaseModelWithRoot


class Rancher(BaseModel):
  class SSH(BaseModel):
    daemon: str = True
    port: PositiveInt = 22

  class State(BaseModel):
    autoformat: Optional[List[Type.Disk.Device]]
    boot_dev: Type.Disk.Label = "LABEL=RANCHER_BOOT"
    boot_fstype: Type.FS = Type.FS.auto
    cryptsetup: bool = False
    dev: Type.Disk.Label = "LABEL=RANCHER_STATE"
    directory: Optional[str]
    fstype: Type.FS = Type.FS.auto
    lvm_scan: bool = False
    mdadm_scan: bool = False
    oem_dev: Type.Disk.Label = "LABEL=RANCHER_OEM"
    oem_fstype: Type.FS = Type.FS.auto
    required: bool = False
    rngd: bool = True
    script: Optional[str]
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

    dns: Optional[DNS] = DNS()
    interfaces: Optional[Interfaces]
    wifi_networks: Optional[WifiNetworks]

  class Environment(BaseModel):
    TZ: str = r"Europe/Moscow"

  class Docker(BaseModel):
    engine: Optional[constr(regex=r"^docker-[0-9]+\.[0-9]+\.[0-9]+$")]

  services_include: ServicesInclude = ServicesInclude()
  network: Optional[Network] = Network()
  environment: Optional[Environment] = Environment()
  runcmd: Optional[List[Union[str, List[str]]]]
  ssh: Optional[SSH] = SSH()
  state: Optional[State] = State()
  preload_wait: bool = True
  docker: Optional[Docker]
