"""Configurações centralizadas para o Gerador de Manuais Automático."""

from dataclasses import dataclass


@dataclass
class AppConfig:
    app_name: str = "Gerador de Manuais Automático"
    app_version: str = "1.0.0"


config = AppConfig()


def get_config() -> AppConfig:
    return config
