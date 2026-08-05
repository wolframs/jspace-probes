#!/bin/sh
# Screenshot the dashboard headlessly, for comparing skins.
#
#   ./snap.sh <out-name> [skin] [theme] [hash]
#
# e.g.  ./snap.sh paper-dark paper dark
#       ./snap.sh paper-rec  paper light '#u9b-a0420-q27b'
#
# Writes out/<out-name>.png (chromium can only write under $HOME).
# Needs ./serve.sh running on :8321. `theme` is forced via the ?theme= param,
# which also freezes the background canvas — deliberate, so shots are stable.
set -e
cd "$(dirname "$0")"
NAME="${1:?usage: snap.sh <out-name> [skin] [theme] [hash]}"
SKIN="$2"
THEME="${3:-dark}"
HASH="$4"
Q="?theme=$THEME"
[ -n "$SKIN" ] && Q="$Q&skin=$SKIN"
mkdir -p out
chromium --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1440,1000 --virtual-time-budget=4000 \
  --screenshot="$PWD/out/$NAME.png" \
  "http://localhost:8321/dashboard/$Q$HASH" 2>/dev/null
echo "out/$NAME.png"
