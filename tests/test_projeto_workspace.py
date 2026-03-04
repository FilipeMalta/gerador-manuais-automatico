"""
Testes unitários para src.projeto (workspace de projeto).

Não dependem de Streamlit — usam stubs simples para UploadedFileLike.
"""

import json
import pytest
from pathlib import Path

from src.projeto import (
    ASSETS_SUBDIR,
    MANUAL_JSON_NAME,
    create_project_dir,
    load_manual_json,
    save_uploaded_file,
    write_manual_json,
)


# ---------------------------------------------------------------------------
# Stub de UploadedFile (sem Streamlit)
# ---------------------------------------------------------------------------

class FakeUploadedFile:
    """Stub mínimo compatível com UploadedFileLike."""

    def __init__(self, name: str, content: bytes):
        self.name = name
        self._content = content

    def read(self) -> bytes:
        return self._content


# ---------------------------------------------------------------------------
# create_project_dir
# ---------------------------------------------------------------------------

class TestCreateProjectDir:
    def test_cria_diretorio_do_projeto(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "proj-1")
        assert project_dir.exists()
        assert project_dir == tmp_path / "proj-1"

    def test_cria_subpasta_assets(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "proj-1")
        assert (project_dir / ASSETS_SUBDIR).is_dir()

    def test_idempotente(self, tmp_path):
        """Chamar duas vezes não levanta exceção."""
        create_project_dir(tmp_path, "proj-x")
        project_dir = create_project_dir(tmp_path, "proj-x")
        assert project_dir.exists()


# ---------------------------------------------------------------------------
# save_uploaded_file
# ---------------------------------------------------------------------------

class TestSaveUploadedFile:
    def test_grava_em_assets(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        fake = FakeUploadedFile("screenshot.png", b"\x89PNG fake")

        rel_path = save_uploaded_file(project_dir, fake, kind="print")

        assert rel_path == f"{ASSETS_SUBDIR}/screenshot.png"
        assert (project_dir / rel_path).exists()

    def test_conteudo_gravado_corretamente(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        content = b"\x89PNG\r\n\x1a\ncontent"
        fake = FakeUploadedFile("img.png", content)

        rel_path = save_uploaded_file(project_dir, fake)

        assert (project_dir / rel_path).read_bytes() == content

    def test_logo_tambem_salva_em_assets(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        fake = FakeUploadedFile("logo.png", b"logo-bytes")

        rel_path = save_uploaded_file(project_dir, fake, kind="logo")

        assert rel_path.startswith(ASSETS_SUBDIR + "/")
        assert (project_dir / rel_path).exists()

    def test_retorna_string(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        fake = FakeUploadedFile("x.png", b"x")
        result = save_uploaded_file(project_dir, fake)
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# write_manual_json / load_manual_json
# ---------------------------------------------------------------------------

DADOS_EXEMPLO = {
    "metadata": {
        "nome_manual": "Manual Teste",
        "modulo": "Módulo X",
        "elaborado": "01/01/2025",
        "revisado": "01/01/2025",
        "classificacao": "interna",
    },
    "objetivo": "Objetivo de teste.",
    "pre_requisito": "Nenhum.",
    "funcionalidades": [
        {
            "titulo": "Func A",
            "descricao": "Descrição A.",
            "prints": ["assets/img.png"],
            "observacoes": [],
        }
    ],
}


class TestWriteLoadManualJson:
    def test_write_cria_arquivo(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        path = write_manual_json(project_dir, DADOS_EXEMPLO)
        assert path.exists()
        assert path.name == MANUAL_JSON_NAME

    def test_load_retorna_mesmo_conteudo(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        write_manual_json(project_dir, DADOS_EXEMPLO)
        carregado = load_manual_json(project_dir)
        assert carregado == DADOS_EXEMPLO

    def test_json_e_utf8_valido(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        dados_unicode = {**DADOS_EXEMPLO, "objetivo": "Ação de configuração é válida."}
        write_manual_json(project_dir, dados_unicode)
        carregado = load_manual_json(project_dir)
        assert "Ação" in carregado["objetivo"]

    def test_load_levanta_se_nao_existe(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        with pytest.raises(FileNotFoundError):
            load_manual_json(project_dir)

    def test_write_retorna_path(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        result = write_manual_json(project_dir, DADOS_EXEMPLO)
        assert isinstance(result, Path)
