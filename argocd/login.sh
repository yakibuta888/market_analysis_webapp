#!/bin/bash

# ArgoCDのサーバーにポートフォワーディングを設定
kubectl port-forward svc/argocd-server -n argocd 8080:443 &

# バックグラウンドプロセスのPIDを取得
PF_PID=$!

# 少し待ってからパスワードを取得
sleep 5
PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode)

# ArgoCDにログイン
# --insecureオプションは自己署名証明書などの場合に必要です
argocd login localhost:8080 --username admin --password "$PASSWORD" --insecure

# スクリプトが終了するときにポートフォワーディングを停止
trap "kill $PF_PID" EXIT

# スクリプトがフォアグラウンドで実行され続けるように待機
# 実際のスクリプトではこの部分を必要に応じて変更してください
read -p "Press enter to exit"

# ポートフォワーディングのプロセスを終了
kill $PF_PID
