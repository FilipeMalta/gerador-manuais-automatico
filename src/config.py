"""
Configurações centralizadas para o Gerador de Manuais Automático.

Este módulo gerencia todas as configurações da aplicação, especialmente
as relacionadas ao Ollama para correção ortográfica com IA.

Configuração via Variáveis de Ambiente:
    - OLLAMA_BASE_URL: URL base do servidor Ollama (padrão: http://localhost:11434)
    - OLLAMA_MODEL: Modelo LLM a usar (padrão: mixtral)
      Modelos disponíveis: mixtral, neural-chat, mistral, llama2
    - OLLAMA_TIMEOUT: Timeout em segundos (padrão: 30)
    - MAX_TEXTO_CHUNK: Máximo de caracteres por chunk (padrão: 2000)

Exemplo de uso com variáveis de ambiente:
    export OLLAMA_MODEL=neural-chat
    export OLLAMA_TIMEOUT=60
    python -m streamlit run app.py

Ou no Windows PowerShell:
    $env:OLLAMA_MODEL="neural-chat"
    $env:OLLAMA_TIMEOUT="60"
    python -m streamlit run app.py

Ou no Windows CMD:
    set OLLAMA_MODEL=neural-chat
    set OLLAMA_TIMEOUT=60
    python -m streamlit run app.py
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class OllamaConfig:
    """Configuração do servidor Ollama para correção ortográfica com IA.
    
    Attributes:
        base_url: URL base do servidor Ollama (padrão: http://localhost:11434)
        model: Modelo LLM a usar (padrão: mixtral)
        timeout: Timeout para requisições em segundos (padrão: 30)
        max_texto_chunk: Máximo de caracteres por chunk de texto (padrão: 2000)
    """
    
    base_url: str = "http://localhost:11434"
    model: str = "mixtral"
    timeout: int = 30
    max_texto_chunk: int = 2000
    
    @classmethod
    def from_env(cls) -> "OllamaConfig":
        """Carrega configurações a partir de variáveis de ambiente.
        
        Valores padrão são usados se as variáveis não estiverem definidas.
        
        Returns:
            OllamaConfig: Instância com valores carregados do ambiente.
        """
        return cls(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            model=os.getenv("OLLAMA_MODEL", "mixtral"),
            timeout=int(os.getenv("OLLAMA_TIMEOUT", "30")),
            max_texto_chunk=int(os.getenv("MAX_TEXTO_CHUNK", "2000"))
        )


@dataclass
class AppConfig:
    """Configuração geral da aplicação.
    
    Attributes:
        app_name: Nome da aplicação
        app_version: Versão da aplicação
        ollama: Configurações específicas do Ollama
    """
    
    app_name: str = "Gerador de Manuais Automático"
    app_version: str = "1.0.0"
    ollama: OllamaConfig = None
    
    def __post_init__(self):
        """Inicializa configurações após criação da instância."""
        if self.ollama is None:
            self.ollama = OllamaConfig.from_env()


# Instância global de configuração
# Carregada automaticamente ao importar este módulo
config = AppConfig()


def get_config() -> AppConfig:
    """Retorna a instância global de configuração.
    
    Returns:
        AppConfig: Configuração da aplicação.
    
    Example:
        >>> from src.config import get_config
        >>> cfg = get_config()
        >>> print(cfg.ollama.model)
        'mixtral'
    """
    return config


def get_ollama_config() -> OllamaConfig:
    """Retorna a configuração específica do Ollama.
    
    Returns:
        OllamaConfig: Configuração do Ollama.
    
    Example:
        >>> from src.config import get_ollama_config
        >>> ollama_cfg = get_ollama_config()
        >>> print(ollama_cfg.base_url)
        'http://localhost:11434'
    """
    return config.ollama


# Configurações predefinidas para referência
MODELOS_OLLAMA_DISPONIVEIS = [
    "mixtral",      # Padrão: melhor balanço velocidade/qualidade
    "neural-chat",  # Otimizado para chat/conversação
    "mistral",      # Rápido e preciso
    "llama2"        # Modelo base robusto
]

TEMPO_ESPERA_PADRAO = 30  # segundos
TAMANHO_MAXIMO_CHUNK = 2000  # caracteres


if __name__ == "__main__":
    """Teste das configurações."""
    print("=" * 60)
    print("Configuração do Gerador de Manuais")
    print("=" * 60)
    
    cfg = get_config()
    print(f"\n📱 Aplicação: {cfg.app_name} v{cfg.app_version}")
    print(f"\n🤖 Ollama Configuration:")
    print(f"   Base URL: {cfg.ollama.base_url}")
    print(f"   Modelo: {cfg.ollama.model}")
    print(f"   Timeout: {cfg.ollama.timeout}s")
    print(f"   Tamanho máximo chunk: {cfg.ollama.max_texto_chunk} chars")
    
    print(f"\n📝 Modelos disponíveis: {', '.join(MODELOS_OLLAMA_DISPONIVEIS)}")
    print("\n" + "=" * 60)
