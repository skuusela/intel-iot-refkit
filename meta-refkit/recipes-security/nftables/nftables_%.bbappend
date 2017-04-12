# do not compile in readline support
DEPENDS_remove = "readline"
EXTRA_OECONF_append = " --without-cli"

# require settings in order to work
VIRTUAL-RUNTIME_nftables-settings ?= "nftables-settings-default"
RDEPENDS_${PN} += "${VIRTUAL-RUNTIME_nftables-settings}"
