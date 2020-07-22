from aqua import Aqua
import json, os
# Use Cases
# 1. Get the list of Image Assurance Policies and save them out by name and type

# Get JWT token from Aqua CSP
aqua = Aqua(id='administrator', password='ZmVjYmQ5', host='testdrive677.aquasec.com', port='443', using_tls=True)

# Expected parameters are registry, hosts, containers_app
# Sending zero filters to retrieve entire CSP landscape
ia_policies = aqua.list_image_assurance()
# Print the total running containers and containers running with at least one critical vulnerability
print("Total IA policies: " + str(ia_policies['count']))

print(ia_policies)
if not os.path.exists("ia"):
    os.makedirs("ia")

for p in ia_policies["result"]:
    if not os.path.exists("ia/" + p["assurance_type"]):
        os.makedirs("ia/" + p["assurance_type"])
    with open("ia/" + p["assurance_type"] + "/" + p["name"], 'w') as f:
        json.dump(p,f)







