#!/bin/bash
set -euxo pipefail

# XVFBの起動
if ! pgrep -x Xvfb > /dev/null;
then
  Xvfb :99 -screen 0 1920x1080x24 &
  echo "Xvfb started on display :99."
else
  echo "Xvfb is already running."
fi

# 少し待ってからスクリプトの実行
sleep 5

# 引数として渡されたPythonスクリプトを実行
exec "$@"
