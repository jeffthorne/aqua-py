from aqua import Aqua
import json

# Use Cases
# 1. Get a list of the initial gateways (need gatway name(s) for the Enforcer group)
# 2. Create the Enforcer group

# Get JWT token from Aqua CSP
aqua = Aqua(id='user', password='password', host='192.168.2.9', port='443', using_tls=True)
# Get the gateway(s) that were deployed with installation to use in Enforcer Group creation
list = []
gateways = aqua.servers()
for gateway in gateways:
    list.append(gateway["id"])
# Create the Enforcer Group with the following required parameters
# type, id, logicalname, host_os, service_account, namespace, runtime, token, enforcer_image, enforce, gateways, orchestrator
enforcer = aqua.create_enforcer_group("agent", "enforcer-example", "python-enforcers", "Linux", "aqua-sa", "aqua", "docker", "token", "4.6", True, list, "kubernetes")
# Print the install command for the Enforcer group
print(enforcer["install_command"])