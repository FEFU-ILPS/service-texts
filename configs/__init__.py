from pydantic_settings import BaseSettings, SettingsConfigDict

from .database import DatabaseConfiguration
from .graylog import GraylogConfiguration


class ProjectConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TEXTS_")

    # * Вложенные группы настроек
    database: DatabaseConfiguration = DatabaseConfiguration()
    graylog: GraylogConfiguration = GraylogConfiguration()

    # * Опциональные переменные
    DEBUG_MODE: bool = True
    SERVICE_NAME: str = "ilps-service-texts"


configs = ProjectConfiguration()

__all__ = ("configs",)
