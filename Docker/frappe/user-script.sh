#!/bin/bash
source /scripts/helper-function.sh

set -e

cleanup() {
    echo "Received signal SIGTERM, stopping..."
    if [ -n "$running_script_pid" ]; then
        kill -s SIGTERM "$running_script_pid"
    fi
    exit 0
}

trap cleanup SIGTERM

emer() {
    echo "$@"
    exit 1
}

if [[ -n "$BENCH_START_OFF" ]]; then
    tail -f /dev/null
else
    echo "Starting supervisor.."
    supervisord -c /opt/user/supervisord.conf &
    running_script_pid=$!
    wait $running_script_pid
fi
