#!/usr/bin/env python3

# TODO: allow defining the zones on-the-fly based on the configuration

import os
import sys
import configparser
import re

zonesConfigPaths = ["/usr/lib/firewall/zones.config", "/etc/firewall/zones.config"]
zonesTemplatePath = "/usr/lib/firewall/zones.template"
zonesRulesetPath = "/run/firewall/zones.ruleset"

# get available interfaces
interfaces = os.listdir("/sys/class/net")

# map interfaces to zones according to configuration
config = configparser.ConfigParser()
files = config.read(zonesConfigPaths)

def search_interfaces(key, conf):
    ret = ""
    if "match" in conf:
        if key in conf["match"]:
            r = re.compile(conf["match"][key])
            ifs = ", ".join([i for i in interfaces if r.search(i)])
            ret = "elements = { " + ifs + " }"

    return ret

# run regexps on the interfaces
local_ifs = search_interfaces("ZONE_LOCAL", config)
lan_ifs = search_interfaces("ZONE_LAN", config)
wan_ifs = search_interfaces("ZONE_WAN", config)
dmz_ifs = search_interfaces("ZONE_DMZ", config)
vpn_ifs = search_interfaces("ZONE_VPN", config)
all_ifs = search_interfaces("ZONE_ALL", config)

# read the template
with open(zonesTemplatePath, "r") as f:
    data = f.read()

output_data = data.format(local_interfaces=local_ifs, lan_interfaces=lan_ifs,
        wan_interfaces=wan_ifs, dmz_interfaces=dmz_ifs,
        vpn_interfaces=vpn_ifs, all_interfaces=all_ifs)

# Do not write the ruleset file if it already exists and there is no change.
# This prevents unneccessary firewall setup changes.
if (os.path.exists(zonesRulesetPath)):
    with open(zonesRulesetPath, "r", encoding="utf-8") as f:
        current_data = f.read()
    if current_data == output_data:
        # same file content
        sys.exit()

# write the ruleset file
with open(zonesRulesetPath, "w") as f:
    f.write(output_data)
