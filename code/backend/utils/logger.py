import logging
import logging.config
from pathlib import Path

# 确保日志目录存在
log_path = Path('logs')
log_path.mkdir(parents=True, exist_ok=True)

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_path / "example.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 1,
            "encoding": "utf-8",
            "formatter": "default",
            "level": "INFO",  # 只记录 INFO 及以上（但不包括 ERROR 单独处理）
        },
        "error_file": {  # 👈 新增：专门记录 ERROR 及以上
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_path / "error.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
            "encoding": "utf-8",
            "formatter": "default",
            "level": "ERROR",  # 只处理 ERROR 和 CRITICAL
        },
        "evaluate_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_path / "evaluate.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
            "encoding": "utf-8",
            "formatter": "default",
            "level": "INFO",
        }
    },
    "loggers": {
        "evaluate_file": {
            "handlers": ["evaluate_file", "error_file"],  # 👈 如果 evaluate 的 error 也要进 error.log
            "level": "INFO",
            "propagate": False,
        }
    },
    "root": {
        # "handlers": ["file", "error_file"],  # 👈 同时写入 example.log 和 error.log
        "handlers": ["file"],  # 👈 只写入 example.log
        "level": "INFO",
    }
}

logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger(__name__)
evaluate_logger = logging.getLogger("evaluate_file")