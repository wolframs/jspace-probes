#!/bin/sh
# Serve the lab: dashboard at http://localhost:8321/dashboard/
cd "$(dirname "$0")"
exec python3 -m http.server 8321
