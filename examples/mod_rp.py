from aqua import Aqua
import json, os
# Use Cases
# Get a named policy by name, modify it and put it back

# Get JWT token from Aqua CSP
aqua = Aqua(id='apiuser', password='apiuserpassword', host='aqua.yourdomain.com', port='443', using_tls=True)

# Get the policy named CIS.  I could use list policies to get all the names but I already know the name of this one

rp_policy = aqua.get_runtime_policies("CIS")

# Print the total running containers and containers running with at least one critical vulnerability
print("Policy received: " + str(rp_policy))

# Change enable_fork_guard: true
rp_policy["enable_fork_guard"]=True
rp_policy["fork_guard_process_limit"]=100


print("Policy modified: " + str(rp_policy))

# Save for post debug and viewing (optional)
with open("tmp_policy", 'w') as f:
    json.dump(rp_policy,f)

resp = aqua.modify_runtime_policies("CIS", json.dumps(rp_policy))

print (str(resp))





