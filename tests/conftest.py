"""
Configuração do pytest para o Gerador de Manuais Automático.
"""

import pytest
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_fixture():
    """Retorna o caminho raiz do projeto para uso em testes."""
    return Path(__file__).parent.parent


def pytest_configure(config):
    """Hook do pytest para configuração inicial."""
    config.addinivalue_line(
        "markers", "unit: marca testes que não precisam dependências externas"
    )
