from ncclient import manager
import yaml
import xml.dom.minidom 

with open ("interfaces_filter.xml","r") as f:
    interfaces_filter = f.read()

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
            
            print("\nFetching running configuration...")
            
            response = m.get_config(source="running" , filter=interfaces_filter)
            
            parsed_xml = xml.dom.minidom.parseString(response.data_xml)
            
            print(parsed_xml.toprettyxml(indent = "  "))
            
           
    except Exception as e :
        print(f"connection failed : {e}")
        

    