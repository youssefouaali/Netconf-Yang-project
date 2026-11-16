from ncclient import manager
import yaml
import sys
with open("devices.yml","r") as f:
    invetory = yaml.safe_load(f)
    
for device in invetory["devices"] :
    try :
        print(f"connecting to {device["name"]}")
        
        netconf_args = {
            "host": device["host"],
            "port": device.get("port", 830),
            "username": device["username"],
            "password": device["password"],
            "hostkey_verify": False,
            "device_params": {"name": device.get("vendor", "default")}
        }
        
        with manager.connect(**netconf_args) as m :
            print ("succesfuly connected to netconf (ssh)") 
            
        
                
            print("fetching running config")
            response = m.get_config(source="running")
            print(response.data_xml)
            
    except Exception as e :
        print(f"connection failed : {e}")
        

    