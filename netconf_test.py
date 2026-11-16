from ncclient import manager
import yaml
import xml.dom.minidom
import os 

interfaces_filter = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="http://openconfig.net/yang/interfaces"/>
</filter>
"""
script_dir = os.path.dirname(os.path.abspath(__file__))
yang_path = os.path.join(script_dir, "openconfig-interfaces.yang")
with open("devices.yml","r") as f:
    inventory = yaml.safe_load(f)
    
for device in inventory["devices"] :
    try :
        print(f"connecting to {device['name']}")
        
        netconf_args = {
            "host": device['host'],
            "port": device.get("port", 830),
            "username": device["username"],
            "password": device["password"],
            "hostkey_verify": False,
        }
        
        with manager.connect(**netconf_args) as m :
            print ("succesfuly connected to netconf (ssh)") 
            
            for cap in m.server_capabilities:
                        print(cap)

            print("\nFetching running configuration...")
            response = m.get_config(source="running" , filter=interfaces_filter)
            
            parsed_xml = xml.dom.minidom.parseString(response.data_xml)
            
            print(parsed_xml.toprettyxml(indent = "  "))
            
            if device["name"] == inventory["devices"][0]["name"]:
                try:
                    schema_reply = m.get_schema("openconfig-interfaces")
                    with open(yang_path, "w") as yf:
                        yf.write(schema_reply.data)
                    print(f"Saved YANG schema to: {yang_path}")
                except Exception as schema_err:
                    print(f"Node does not support get_schema download: {schema_err}")
            
    except Exception as e :
        print(f"connection failed : {e}")
        

    