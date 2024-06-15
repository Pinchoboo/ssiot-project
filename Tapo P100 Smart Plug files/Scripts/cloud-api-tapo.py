# Script for contacting the TPLink cloud service to retrieve info for all devices linked with the TPLink account.

# For installation and more on https://pypi.org/project/tplink-cloud-api/

from tplinkcloud import TPLinkDeviceManager
import json
import asyncio

username='username@test.com'
password='test_password'
device_manager = TPLinkDeviceManager(username, password)

async def fetch_all_devices_sys_info():
  devices = await device_manager.get_devices()
  fetch_tasks = []
  for device in devices:
    async def get_info(device):
      print(f'Found {device.model_type.name} device: {device.get_alias()}')
      print("SYS INFO")
      print(json.dumps(device.device_info, indent=2, default=lambda x: vars(x)
                        if hasattr(x, "__dict__") else x.name if hasattr(x, "name") else None))
      print(json.dumps(await device.get_sys_info(), indent=2, default=lambda x: vars(x)
                        if hasattr(x, "__dict__") else x.name if hasattr(x, "name") else None))
    fetch_tasks.append(get_info(device))
  await asyncio.gather(*fetch_tasks)

asyncio.run(fetch_all_devices_sys_info())
