"""
Sistema centralizado de logging para o Gerador de Manuais Automático.

Este módulo configura e fornece um logger centralizado para toda a aplicação,
com suporte a logs em arquivo e console.

Uso:
    from src.logger import get_logger
    
    logger = get_logger(__name__)
    logger.info("Mensagem informativa")
    logger.warning("Aviso")
    logger.error("Erro")
    logger.debug("Debug")

Formato de Log:
    2026-02-10 15:30:45,123 | INFO | app | Mensagem de informação
    2026-02-10 15:30:45,456 | ERROR | correcao_ortografica | Erro ao conectar

Configuração:
    - Diretório de logs: logs/
    - Arquivo: logs/app.log
    - Nível padrão: INFO
    - Rotação: Automática (máxx 5MB por arquivo, até 5 backups)
"""

import logging
import logging.handlers
from pathlib import Path
import os
from typing import Optional


# Diretório de logs
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOGS_DIR / "app.log"

# Criar diretório se não existir
LOGS_DIR.mkdir(exist_ok=True)


# Formato padrão de logs
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _criar_logger_base() -> logging.Logger:
    """
    Cria e configura o logger base da aplicação.
    
    Returns:
        logging.Logger: Logger configurado com handlers para arquivo e console.
    """
    logger = logging.getLogger("gerador_manuais")
    logger.setLevel(logging.DEBUG)
    
    # Remover handlers existentes para evitar duplicação
    logger.handlers.clear()
    
    # Formatter padrão
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    
    # ==================== Handler para Arquivo ====================
    # Usar RotatingFileHandler para limitar tamanho do arquivo
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,              # Manter 5 backups
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # ==================== Handler para Console ====================
    # Mostrar apenas WARNING e acima no console durante execução normal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Instância global base
_LOGGER_BASE = _criar_logger_base()


def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger específico para um módulo.
    
    Args:
        name: Nome do módulo (normalmente __name__)
        
    Returns:
        logging.Logger: Logger configurado para o módulo
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Iniciando aplicação")
    """
    return logging.getLogger(f"gerador_manuais.{name}")


def set_debug_mode(enabled: bool = True) -> None:
    """
    Ativa ou desativa o modo debug.
    
    Em modo debug, mensagens DEBUG aparecem também no console.
    
    Args:
        enabled: True para ativar debug, False para desativar
        
    Example:
        >>> set_debug_mode(True)
        >>> logger = get_logger(__name__)
        >>> logger.debug("Esta mensagem aparecerá no console")
    """
    base_logger = logging.getLogger("gerador_manuais")
    
    for handler in base_logger.handlers:
        if isinstance(handler, logging.StreamHandler) and \
           not isinstance(handler, logging.FileHandler):
            if enabled:
                handler.setLevel(logging.DEBUG)
            else:
                handler.setLevel(logging.WARNING)


def get_log_file_path() -> Path:
    """
    Retorna o caminho do arquivo de log.
    
    Returns:
        Path: Caminho para logs/app.log
        
    Example:
        >>> log_path = get_log_file_path()
        >>> print(f"Logs salvos em: {log_path}")
    """
    return LOG_FILE


def log_informacoes_sistema() -> None:
    """
    Registra informações do sistema na inicialização.
    
    Inclui:
    - Versão do Python
    - Caminho de execução
    - Data/hora
    """
    import sys
    import platform
    
    logger = get_logger(__name__)
    
    logger.info("=" * 80)
    logger.info("🚀 Gerador de Manuais Automático - Iniciando")
    logger.info("=" * 80)
    logger.info(f"Sistema operacional: {platform.system()} {platform.release()}")
    logger.info(f"Python: {sys.version}")
    logger.info(f"Arquivo de log: {LOG_FILE}")
    logger.info("=" * 80)


if __name__ == "__main__":
    """Teste do sistema de logging."""
    
    # Ativar modo debug para mostrar tudo no console
    set_debug_mode(True)
    
    logger = get_logger(__name__)
    
    print("🧪 Testando Sistema de Logging\n")
    
    logger.debug("Mensagem de DEBUG")
    logger.info("Mensagem de INFO")
    logger.warning("Mensagem de WARNING")
    logger.error("Mensagem de ERROR")
    
    print(f"\n✅ Logs salvos em: {get_log_file_path()}")
    
    # Mostrar conteúdo do arquivo
    if LOG_FILE.exists():
        print(f"\n📄 Conteúdo de {LOG_FILE.name}:\n")
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            print(f.read())
