from dataclasses import dataclass
import subprocess, re

@dataclass
class Device:
    serial: str
    uri_usb: str

_ADDR_RE = re.compile(r'\d+:.*')
_SERIAL_RE = re.compile(r'[\d|a-f]{34}')
_USB_RE = re.compile(r'usb:\d+\.\d+\.\d+')

def get_devices():
    presult = subprocess.run(R'iio_info -S', shell=True, stdout=subprocess.PIPE)
    lines = presult.stdout.decode('utf-8').splitlines()
    list = []
    for line in lines:
        stdout = line.strip()
        if not _ADDR_RE.fullmatch(stdout):
            continue
        serial = _SERIAL_RE.search(stdout)
        uri_usb = _USB_RE.search(stdout)
        if serial == None or uri_usb == None:
            continue
        list.append(Device(serial.group(), uri_usb.group()))
    return list

def find_device(serial: str, devices: list[Device]) -> Device:
    for device in devices:
        # 文字列後方一致
        if device.serial[-len(serial):] == serial:
            return device
    raise Exception("device not found")
