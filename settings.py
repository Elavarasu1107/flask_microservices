from pydantic import PostgresDsn, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore', env_file='.env')
    config_mode: str
    development_database_url: PostgresDsn
    algorithm: str
    jwt_key: str
    base_url: str
    user_port: int
    celery_broker: str
    celery_result: str
    admin_key: str
    email_host_user: EmailStr
    email_host_password: str
    smtp: str
    smtp_port: int


settings = Settings()

# logging.basicConfig(filename='fundoo.log', encoding='utf-8', level=logging.WARNING,
#                     format='%(asctime)s:%(filename)s:%(levelname)s:%(lineno)d:%(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p')
# logger = logging.getLogger()
