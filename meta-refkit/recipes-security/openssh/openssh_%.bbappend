FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

RDEPENDS_${PN}-sshd += "nftables"

SRC_URI_append = "\
    file://openssh-sshd.ruleset \
"

do_install_append() {
    install -d ${D}${libdir}/firewall/services
    install -m 0644 ${WORKDIR}/openssh-sshd.ruleset ${D}${libdir}/firewall/services/
}

FILES_${PN} += " \
    ${libdir}/firewall/services/openssh-sshd.ruleset \
"
