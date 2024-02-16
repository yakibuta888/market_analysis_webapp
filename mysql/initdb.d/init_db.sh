#!/bin/bash
set -e

# MySQLサービスが起動するのを待つ
# MySQLサーバーへの接続情報
host="localhost"
user="root"
password="${MYSQL_ROOT_PASSWORD}" # Dockerで設定された環境変数
port="3306"

# MySQLサーバーが起動して接続可能になるまで待機
echo "Waiting for MySQL to start..."
while ! mysqladmin ping -h"$host" -u"$user" -p"$password" --silent; do
    echo "MySQL is not up yet... waiting..."
    sleep 1
done

echo "MySQL started."

# 環境変数からデータベース名、ユーザー名、パスワードを取得
# MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD はDockerコンテナ起動時に指定
DB_NAME=${MYSQL_DATABASE:-myapp}
DB_USER=${MYSQL_USER:-myappuser}
DB_PASSWORD=${MYSQL_PASSWORD:-mypassword}

# データベースの作成
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
    CREATE DATABASE IF NOT EXISTS $DB_NAME DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EOSQL

# ユーザーの作成と権限の設定
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
    CREATE USER IF NOT EXISTS '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';
    GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';
    FLUSH PRIVILEGES;
EOSQL
