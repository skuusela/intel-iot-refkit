#!/bin/sh
DEFAULT_SSH_RULE="tcp dport ssh iif @ZONE_LAN mark set 0x00000001"
HANDLE=$(nft list ruleset -a | grep "$DEFAULT_SSH_RULE"| awk '{print $NF}')
nft replace rule inet filter openssh-sshd handle $HANDLE \
tcp dport ssh iif @ZONE_LAN mark set 0x00000003

sleep 5

nft replace rule inet filter openssh-sshd handle $HANDLE $DEFAULT_SSH_RULE
