from ncclient import manager
import yaml
import time


with open("playloads/dhcp_config.xml","r") as f:
    interface_playload = f.read()

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
         
        if ":candidate" not in m.server_capabilities :
            print(f"{device['name']} does not support the candidate datastores. ")
            continue
        with m.locked(target="candidate") :
            print("locked candidate datastores . pushing draft config...")
            
            m.edit_config(target="candidate", config= interface_playload)
            
            if ":validate:1.1" in m.server_capabilities or ":validate:1.0" in m.server_capabilities :
                m.validate(source="candidate")
                print("CANDIDATE CONFIG VALIDATED !")
            
            print("Applying with 60s confirmed-commit timer...")
            m.commit(confirmed=True,timeout="60")
            
            time.sleep(2)
            m.get_config(source="running")
            
            m.commit()
            print(f"--------------SUCCESSFULLY created and confirmed on {device["name"]} !-------------")
            
        
    except Exception as e :
        print(f"connection failed on {device["name"]} : {e}")
        print("if a confirmed commit was triggered  , the switch will auto-rollback in 60s . ")     