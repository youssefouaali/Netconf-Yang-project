from ncclient import manager
import yaml

with open("devices.yml","r") as f:
    inventory = yaml.safe_load(f)

for device in inventory["devices"] :
    with manager.connect(
        host=device["host"],
        port=830,
        username=device["username"],
        password=device["password"],
        hostkey_verify=False,
        device_params={"name": "default"}
    ) as m:
        try:
            schema_reply = m.get_schema("openconfig-interfaces")
            with open("openconfig-interfaces.yang","w")  as yf:
                yf.write(schema_reply.data)    
        except Exception as schema_err:
                 print(f"Node does not support get_schema download: {schema_err}")
            