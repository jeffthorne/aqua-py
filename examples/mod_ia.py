from aqua import Aqua
import json, os
# Use Cases
# Get a named policy by name, modify it and put it back

# Get JWT token from Aqua CSP
aqua = Aqua(id='apiuser', password='apiuserpassword', host='aqua.yourdomain.com', port='443', using_tls=True)

# Get the policy named Aqua-Demo.  I could use list policies to get all the names but I already know the name of this one

ia_policy = aqua.get_image_assurance("Aqua-Demo","image")

# Print the total running containers and containers running with at least one critical vulnerability
print("Policy received: " + str(ia_policy))

# Change scan_sensitive_data: true
ia_policy["scan_sensitive_data"]=True

print("Policy modified: " + str(ia_policy))

with open("tmp_policy", 'w') as f:
    json.dump(ia_policy,f)

policy_type=ia_policy["assurance_type"]
resp = aqua.modify_image_assurance("Aqua-Demo", json.dumps(ia_policy), policy_type)

print (str(resp))





