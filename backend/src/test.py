import logging

# ログレベル、フォーマット、ファイル名などを直接指定
logging.basicConfig(level=logging.INFO,
                    filename='/home/client/app/src/log/app.log',
                    filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s')

# ロガーを取得してログメッセージを出力
logger = logging.getLogger(__name__)
logger.info('これはテストメッセージです。')
