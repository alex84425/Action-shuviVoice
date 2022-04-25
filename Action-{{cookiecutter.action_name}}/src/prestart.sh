#! /usr/bin/env sh

## start uut-operation-proxy at default 8888
mkdir -p /data/log
/opt/uut-operation-proxy-linux >/data/log/uut_proxy.log 2>&1 &
