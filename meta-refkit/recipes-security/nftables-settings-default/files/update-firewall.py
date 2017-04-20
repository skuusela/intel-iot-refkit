#!/usr/bin/env python3

import os
import fcntl

servicePaths = ["/usr/lib/firewall/services", "/etc/firewall/services"]
configTemplatePath = "/usr/lib/firewall/firewall.template"
configRulesetPath = "/run/firewall/firewall.ruleset"

# lock to prevent processing several events at once
lock = open("/run/firewall/config_flock", "w")
fcntl.lockf(lock, fcntl.LOCK_EX)

# read the template
with open(configTemplatePath, "r") as f:
    data = f.read()

serviceFiles = []
for path in list(filter(os.path.exists, servicePaths)):
    serviceFiles += [os.path.realpath(path + "/" + f) for f in os.listdir(path)]

service_file_blob = "\n".join(["include \"" + f + "\"" for f in serviceFiles])

output_data = data.format(service_chains=service_file_blob)

# write the ruleset file
with open(configRulesetPath, "w") as f:
    f.write(output_data)
