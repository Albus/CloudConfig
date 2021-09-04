```python
import os
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler

from CloudConfig import Config
from CloudConfig.Rancher import Rancher
from CloudConfig.WriteFiles import WriteFiles

obj = Config(hostname=r"docker")

obj.rancher.services_include.hyperv_vm_tools = True
obj.rancher.services_include.container_cron = True
obj.rancher.services_include.kernel_extras = True
obj.rancher.services_include.kernel_headers = True
obj.rancher.services_include.kernel_headers_system_docker = True
obj.rancher.services_include.zfs = True
obj.rancher.services_include.volume_cifs = True

obj.ssh_authorized_keys = [
  "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCg4HkhiEGVFuE/IY6VpLWlP7ARvDDOyNip796hIRXCxsi3rQxVrpV+5DssDqM/rwCTz"
  "/ROEz0a8B3UOfXFmfu4jgSMuBeu08Y/No+iOk7vra9E/NotiSxLHvpzO2BFCNkdfCN9A+kaRyiPxy19QAUVKFukQqrxwotDo4XTb0I/fb"
  "+T4jNPyqIPlxafnrn9Awu5xn9Z7B+d35FXoaYIxm4pjMg6UPh2iDqBrJ65XF1629e9pgfnWguj"
  "/l4vNCmXpLrUlJfe3mbqeZT9k1cdu7t4UlJZE2MDFBe46NsUU9C9J5Uxocma7IljTupImhcS5YF8QdHvDabbUlALIZgShRWh"]
obj.rancher.state.autoformat = [r"/dev/sda"]
obj.rancher.network.interfaces = {
  r"eth0": Rancher.Network.Interfaces.eth(),
  r"eth1": Rancher.Network.Interfaces.eth(dhcp=False, address=r"192.168.3.2/24")
}  # type: Rancher.Network.Interfaces

obj.write_files = [
  WriteFiles(path=r"/etc/environment",
             append=True,
             permissions="0644",
             content=os.linesep + 'TZ="Europe/Moscow"')
]

data = obj.json(by_alias=True, exclude_none=True)


class _RequestHandler(BaseHTTPRequestHandler):

  def _set_headers(self):
    self.send_response(HTTPStatus.OK.value)
    self.send_header(r'Content-type', r'application/json')
    self.end_headers()

  def do_GET(self):
    self._set_headers()
    self.wfile.write(data.encode())


def run_server():
  server_address = (r'0.0.0.0', 8001)
  httpd = HTTPServer(server_address, _RequestHandler)
  print(r'serving at http://%s:%d' % server_address)
  httpd.serve_forever()


if __name__ == r'__main__':
  run_server()


```

```shell
# sudo ros install -d /dev/sda -c http://192.168.0.1:8001 
```