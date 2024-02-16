# run_alembic.py
import os
import subprocess
from config import generate_alembic_config


COMMAND = ["alembic", "revision", "--autogenerate", "-m", "Initial database setup"]


def run_command_with_progress(command: list[str]):
    # コマンドを開始
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        # 標準出力と標準エラー出力をリアルタイムで処理
        while True:
            output = process.stdout.readline() if process.stdout is not None else None
            if output:
                print(output.strip())
            error_output = process.stderr.readline() if process.stderr is not None else None
            if error_output:
                print(f"Error: {error_output.strip()}")

            # プロセスが終了したかチェック
            if output == '' and error_output == '' and process.poll() is not None:
                break

        # プロセスの終了コードを確認
        if process.returncode != 0:
            # エラーメッセージの処理
            raise subprocess.CalledProcessError(process.returncode, command)
        else:
            print("Command executed successfully")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        # 必要に応じて、さらに詳細なエラー処理をここに追加


def main():
    # 環境変数から実行環境を取得（デフォルトは開発環境）
    env = os.getenv('APP_ENV', 'development')

    # テスト環境の場合はtestingフラグをTrueに
    testing = env == 'test'

    # Alembic設定ファイルを生成
    generate_alembic_config(testing=testing)

    # Alembicコマンドを実行
    run_command_with_progress(COMMAND)


if __name__ == "__main__":
    main()
