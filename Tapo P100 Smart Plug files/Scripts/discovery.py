# Script to discover the device on the LOCAL network.
# Both the device and the host running the script need to be on the same network.

# For installation and more on https://pypi.org/project/plugp100/

my_plug = {
    "tapoIp": "x.x.x.x",
    "tapoEmail": "username@test.com",
    "tapoPassword": "test_password"
}

import asyncio
import logging
from plugp100.common.credentials import AuthCredential
from plugp100.discovery.tapo_discovery import TapoDiscovery

async def example_discovery(credentials: AuthCredential):
    discovered = await TapoDiscovery.scan(timeout=5)
    for discovered_device in discovered:
        try:
            device = await discovered_device.get_tapo_device(credentials)
            await device.update()
            print({
                'type': type(device),
                'protocol': device.protocol_version,
                'raw_state': device.raw_state
            })
            await device.client.close()
        except Exception as e:
            logging.error(f"Failed to update {discovered_device.ip} {discovered_device.device_type}", exc_info=e)

async def main():
    credentials = AuthCredential(my_plug["tapoEmail"], my_plug["tapoPassword"])
    await example_discovery(credentials)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()
