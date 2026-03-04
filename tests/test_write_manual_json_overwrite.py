"""
Trava que write_manual_json sobrescreve corretamente o arquivo existente.

Cobre quatro critérios:
1. Campo alterado é persistido na segunda gravação.
2. Chaves removidas não acumulam no arquivo.
3. Unicode é preservado após sobrescrita.
4. Múltiplas gravações mantêm apenas a última versão.
"""

import pytest
from src.projeto import create_project_dir, write_manual_json, load_manual_json


class TestWriteManualJsonOverwrite:
    def test_sobrescreve_campo_alterado(self, tmp_path):
        """Salva JSON, altera campo, salva novamente — valor novo é persistido."""
        project_dir = create_project_dir(tmp_path, "p")
        dados = {"nome": "Manual V1", "valor": 1}
        write_manual_json(project_dir, dados)

        dados["valor"] = 99
        write_manual_json(project_dir, dados)

        recarregado = load_manual_json(project_dir)
        assert recarregado["valor"] == 99

    def test_nao_acumula_conteudo(self, tmp_path):
        """Segunda gravação com menos chaves não mantém as antigas (overwrite, não merge)."""
        project_dir = create_project_dir(tmp_path, "p")
        write_manual_json(project_dir, {"a": 1, "b": 2})
        write_manual_json(project_dir, {"a": 1})  # "b" removido

        recarregado = load_manual_json(project_dir)
        assert "b" not in recarregado
        assert recarregado["a"] == 1

    def test_unicode_preservado_apos_sobrescrita(self, tmp_path):
        """Caracteres especiais do português são preservados após sobrescrita."""
        project_dir = create_project_dir(tmp_path, "p")
        write_manual_json(project_dir, {"texto": "versão inicial"})
        write_manual_json(project_dir, {"texto": "versão atualizada com ç, ã, é"})

        recarregado = load_manual_json(project_dir)
        assert recarregado["texto"] == "versão atualizada com ç, ã, é"

    def test_multiplas_gravacoes_mantem_ultimo(self, tmp_path):
        """N gravações consecutivas — apenas o valor da última é lido."""
        project_dir = create_project_dir(tmp_path, "p")
        for i in range(5):
            write_manual_json(project_dir, {"iteration": i})

        recarregado = load_manual_json(project_dir)
        assert recarregado["iteration"] == 4
