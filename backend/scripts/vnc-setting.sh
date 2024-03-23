#!/bin/bash
set -euxo pipefail

FILE=$HOME/.vnc/passwd
if [ -f "$FILE" ]; then
  USER="$(whoami)" vncserver :1 -depth 24 -geometry 800x600 -br -rfbport=5901 -PasswordFile=$HOME/.vnc/passwd
else
  USER="$(whoami)" vncserver :1 -geometry 800x600 -depth 24
fi

if ! lsof -i:80 > /dev/null; then
  websockify -D --web=/usr/share/novnc/ 80 localhost:5901
fi
