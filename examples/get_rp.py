from aqua import Aqua
import json, os
# Use Cases
# 1. Get the list of Image Assurance Policies and save them out by name and type

# Get JWT token from Aqua CSP
aqua = Aqua(id='apiuser', password='apiuserpassword', host='aqua.yourdomain.com', port='443', using_tls=True)

# Expected parameters are registry, hosts, containers_app
# Sending zero filters to retrieve entire CSP landscape
rp_policies = aqua.list_runtime_policies()
# Print the total running containers and containers running with at least one critical vulnerability
print("Total Runtime policies: " + str(rp_policies['count']))

print(rp_policies)
if not os.path.exists("rp"):
    os.makedirs("rp")

for p in rp_policies["result"]:
    if not os.path.exists("rp/" + p["runtime_type"]):
        os.makedirs("rp/" + p["runtime_type"])
    with open("rp/" + p["runtime_type"] + "/" + p["name"], 'w') as f:
        json.dump(p,f)







