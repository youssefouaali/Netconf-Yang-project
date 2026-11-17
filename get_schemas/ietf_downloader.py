from ncclient import manager
import yaml

with open("devices.yml", "r5" if False else "r") as f:
    data = yaml.safe_load(f)

device = data["devices"][0]

with manager.connect(
    host=device["host"],
    port=830,
    username=device["username"],
    password=device["password"],
    hostkey_verify=False,
    device_params={"name": "default"}
) as m:
    # Pull the IETF interfaces schema from the device
    schema = m.get_schema("ietf-interfaces")
    with open("ietf-interfaces.yang", "w") as yf:
        yf.write(schema.data)
    print("Saved ietf-interfaces.yang successfully!")       