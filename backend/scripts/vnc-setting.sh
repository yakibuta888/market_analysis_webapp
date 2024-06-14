#!/bin/bash
set -euxo pipefail

# XVFBの起動
if ! pgrep -x Xvfb > /dev/null;
then
  Xvfb :99 -screen 0 1920x1080x24 &
  echo "Xvfb started."
else
  echo "Xvfb is already running."
fi

# 使用可能なディスプレイ番号を見つける
find_free_display() {
    local display_num=1
    while [ -e "/tmp/.X11-unix/X${display_num}" ]; do
        display_num=$((display_num + 1))
    done
    echo ":${display_num}"
}

# VNCサーバーの設定と起動
DISPLAY_NUM=$(find_free_display)
FILE=$HOME/.vnc/passwd
if ! pgrep -x "Xtigervnc" > /dev/null;
then
  if [ -f "$FILE" ]; then
    USER="$(whoami)" vncserver $DISPLAY_NUM -depth 24 -geometry 1280x720 -br -rfbport=5901 -PasswordFile=$HOME/.vnc/passwd
  else
    USER="$(whoami)" vncserver $DISPLAY_NUM -geometry 1280x720 -depth 24
  fi
  echo "VNC server started on display $DISPLAY_NUM."
else
  echo "VNC server is already running."
fi

# noVNCサーバーの起動
if ! lsof -i:80 > /dev/null; then
  websockify -D --web=/usr/share/novnc/ 80 localhost:5901
  echo "noVNC started."
else
  echo "noVNC is already running."
fi

# xfce4デスクトップ環境の起動
if ! pgrep -x "xfce4-session" > /dev/null;
then
  startxfce4 &
  echo "xfce4 started."
else
  echo "xfce4 is already running."
fi
