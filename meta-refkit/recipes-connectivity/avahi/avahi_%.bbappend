FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

# libnss-mdns is not supported, so remove it from the RRECOMMENDS
RRECOMMENDS_avahi-daemon_remove_libc-glibc = " libnss-mdns"
RRECOMMENDS_${PN}_remove_libc-glibc = " libnss-mdns"

# provide libdns_sd.so and dns_sd.h header
EXTRA_OECONF += "--enable-compat-libdns_sd"

FILES_${PN} += " \
    ${libdir}/libdns_sd.* \
"

# add firewall support
RDEPENDS_${PN} += "nftables"

SRC_URI_append = "\
    file://avahi.ruleset \
"

do_install_append() {
    install -d ${D}${includedir}/avahi-compat-libdns_sd
    install -m 0644 ${S}/avahi-compat-libdns_sd/dns_sd.h ${D}${includedir}/avahi-compat-libdns_sd/

    install -d ${D}${libdir}/firewall/services
    install -m 0644 ${WORKDIR}/avahi.ruleset ${D}${libdir}/firewall/services/
}

FILES_${PN} += " \
    ${libdir}/firewall/services/avahi.ruleset \
"
