import logging
import time
from logging.handlers import RotatingFileHandler

# ロギングの基本設定
logging.basicConfig(level=logging.DEBUG)

# ログファイルを回転させるハンドラを追加
log_handler = RotatingFileHandler("./output/sample.log", maxBytes=1024 * 1024)
log_handler.setLevel(logging.DEBUG)

# ロガーにハンドラを追加
logger = logging.getLogger(__name__)
logger.addHandler(log_handler)

# ログを大量に出力するループ
for i in range(1000000000000):
    logger.debug(f"This is a sample log message #{i}")
    # time.sleep(1)

# ロガーに追加したハンドラをクリーンアップ
logger.removeHandler(log_handler)
