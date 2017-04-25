FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = "\
    file://0001-unit-service-allow-rerunning-reload-tasks.patch \
    file://0002-path-add-ReloadOnTrigger-option.patch \
"

# Prefer systemd way of creating getty@.service symlinks using
# systemd-getty-generator (instead of the Yocto default
# systemd-serialgetty that creates everything in do_install).
PACKAGECONFIG_append = "serial-getty-generator"
