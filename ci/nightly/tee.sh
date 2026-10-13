#!/usr/bin/env bash

logfile="$1"
shift 1

exec > >(tee -ia $logfile) 2>&1

"$@"
result="$?"

sed -i '1d' "$logfile"

exit "$result"
