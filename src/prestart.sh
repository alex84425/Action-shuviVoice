#! /usr/bin/env sh

## start uut-operation-proxy at default 8888
mkdir -p /data/log
/opt/uut-operation-proxy-linux 2>&1 | multilog t s15728640 n20 /data/log &

# Migration (can be remove after 2022 November release)
rm -f /data/log/uut_proxy.log
