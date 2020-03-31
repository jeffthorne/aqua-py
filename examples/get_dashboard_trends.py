from aqua import Aqua
import time
# Use Cases
# 1. Retrieve Trend information for Running Containers, Images and Vulnerabilities

# Get JWT token from Aqua CSP
aqua = Aqua(id='user', password='password', host='192.168.2.9', port='443', using_tls=True)

# Expected parameters the type of trend: containers, vulnerabilities, images

trends = aqua.trends("images")
# Print the image trend statistics
print("Image Statistics\n")
for trend in trends:
    print("Date: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(trend["date"])) + "  Images Scanned: " + str(trend["total"]) + "  Critical Detected: " + str(trend["critical"]) + "  High: " + str(trend["high"]))

trends = aqua.trends("containers")
# Print the container trend statistics
print("\nContainer Statistics\n")
for trend in trends:
    print("Date: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(trend["date"])) + "  Running Containers: " + str(trend["total"]) + "  Critical Detected: " + str(trend["critical"]) + "  High: " + str(trend["high"]))

trends = aqua.trends("vulnerabilities")
# Print the image trend statistics
print("\nVulnerability Statistics\n")
for trend in trends:
    print("Date: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(trend["date"])) + "  Critical Detected: " + str(trend["critical"]) + "  High: " + str(trend["high"]))