# Multi-Device NETCONF Configuration Push (Arista cEOS + Containerlab)

A Python automation script using `ncclient` and YAML inventory (`devices.yml`) to push XML/OpenConfig configuration payloads to multiple network devices over NETCONF/SSH, with capability checks for candidate datastores, validation, and safe commit handling.

## Project Structure

```text
project9/
├── devices.yml              # Device inventory (host, port, credentials, device metadata)
├── push_config.py           # Main NETCONF deployment script
└── payloads/
    ├── dhcp_config.xml      # Static XML configuration payload
    └── ospf_config.xml.j2   # Jinja2 XML template (for dynamic per-device rendering)
