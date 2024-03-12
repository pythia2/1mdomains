#!/usr/bin/env bash

#set -Eeuo pipefail

if [[ $# -ne 1 ]]; then
    echo 'Too many/few arguments, expecting one of (10..100.1000..100000)' >&2
    exit 1
fi

#function process () {
#     head -n${1} mm.txt | xargs --max-procs=0 -I% dig @8.8.8.8 _dmarc.% txt +short +tries=1 +timeout=10; | cat > ${1}-results.txt
#}


function process () {
     head -n${1} mm.txt | xargs --max-procs=0 -I% dig @8.8.8.8 _dmarc.% txt +tries=1 +timeout=10 | grep "v=DMARC1" | cat > ${1}-results.txt
}

FILE="${1}-results.txt"
if test -f $FILE; then
    echo "$FILE exists. moving to $FILE-$(date +%Y-%m-%d_%H-%M)"
    mv $FILE $FILE-$(date +%Y-%m-%d_%H-%M)
fi

echo ""
echo ""
echo ""

time process $1


echo ""
echo ""
echo ""
