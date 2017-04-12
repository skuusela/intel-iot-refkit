# do not compile in readline support
DEPENDS_remove = "readline"
EXTRA_OECONF_append = " --without-cli"
