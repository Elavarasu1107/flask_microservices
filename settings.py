from pydantic import PostgresDsn, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from logging.config import dictConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore', env_file='.env')
    config_mode: str
    development_database_url: PostgresDsn
    algorithm: str
    jwt_key: str
    base_url: str
    user_port: int
    note_port: int
    label_port: int
    celery_broker: str
    celery_result: str
    admin_key: str
    email_host_user: EmailStr
    email_host_password: str
    smtp: str
    smtp_port: int


settings = Settings()


dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s]: %(filename)s: %(levelname)s: %(lineno)d: %(message)s",
            'datefmt': '%m/%d/%Y %I:%M:%S %p'
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "fundoo.log",
            "formatter": "default",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "file_logger": {
            "level": "WARNING",
            "handlers": ['file'],
            "propagate": False
        }
    }
})
