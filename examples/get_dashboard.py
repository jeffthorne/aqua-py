from aqua import Aqua
# Use Cases
# 1. Retrieve the Running Container, Image and Vulnerability statistics for the CSP environment

# Get JWT token from Aqua CSP
aqua = Aqua(id='user', password='password', host='192.168.2.9', port='443', using_tls=True)

# Expected parameters are registry, hosts, containers_app
# Sending zero filters to retrieve entire CSP landscape
dashboard = aqua.dashboard("", "", "")
# Print the total running containers and containers running with at least one critical vulnerability
print("Total Running Containers: " + str(dashboard['running_containers']['total']))
print("Containers Running with a Critical Vulnerability: " + str(dashboard["running_containers"]["critical"]))