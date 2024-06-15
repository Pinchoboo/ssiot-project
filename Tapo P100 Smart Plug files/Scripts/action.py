# Script to turn execute actions on the device LOCALLY.
# Both the device and the host running the script need to be on the same network.

# For installation and more on https://pypi.org/project/plugp100/

import asyncio
from plugp100.common.credentials import AuthCredential
from plugp100.new.device_factory import connect, DeviceConnectConfiguration

my_plug = {
    "tapoIp": "x.x.x.x",
    "tapoEmail": "username@test.com",
    "tapoPassword": "test_password"
}

async def example_connect_by_guessing(credentials: AuthCredential, host: str):
    device_configuration = DeviceConnectConfiguration(
        host=host,
        credentials=credentials
    )
    device = await connect(device_configuration)
    await device.update()
    print({
        'type': type(device),
        'protocol': device.protocol_version,
        'raw_state': device.raw_state,
        'components': device.get_device_components
    })
    print(device)
    await device.turn_off()
    await device.turn_on()

async def main():
    credentials = AuthCredential(my_plug["tapoEmail"], my_plug["tapoPassword"])
    await example_connect_by_guessing(credentials, my_plug["tapoIp"])

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()
