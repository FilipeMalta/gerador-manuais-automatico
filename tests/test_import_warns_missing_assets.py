"""
Trava o comportamento de find_missing_assets:
- Retorna lista vazia quando todos os prints existem.
- Detecta prints referenciados mas ausentes em disco.
- Funciona corretamente após import_project_zip (zip sem os assets).
- Ignora funcionalidades sem prints.
- Retorna lista vazia quando manual.json não existe.
"""

import io
import json
import zipfile

import pytest
from pathlib import Path
from PIL import Image

from src.projeto import ASSETS_SUBDIR, MANUAL_JSON_NAME, create_project_dir, write_manual_json
from src.projeto_zip import find_missing_assets, import_project_zip


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_META = {
    "nome_manual": "Manual Assets",
    "modulo": "Assets",
    "elaborado": "01/01/2025",
    "revisado": "01/01/2025",
    "classificacao": "interna",
}


def _dados_com_prints(*rel_paths: str) -> dict:
    return {
        "metadata": _META,
        "objetivo": "Obj.",
        "pre_requisito": "Nenhum.",
        "funcionalidades": [
            {
                "titulo": "Func",
                "descricao": "Desc.",
                "prints": list(rel_paths),
                "observacoes": [],
            }
        ],
    }


def _make_png_bytes() -> bytes:
    import io as _io
    img = Image.new("RGB", (10, 10), color=(255, 0, 0))
    buf = _io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Testes de find_missing_assets
# ---------------------------------------------------------------------------

class TestFindMissingAssets:
    def test_lista_vazia_quando_todos_presentes(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        (project_dir / ASSETS_SUBDIR / "img.png").write_bytes(_make_png_bytes())
        write_manual_json(project_dir, _dados_com_prints("assets/img.png"))

        assert find_missing_assets(project_dir) == []

    def test_detecta_print_ausente(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        write_manual_json(project_dir, _dados_com_prints("assets/nao_existe.png"))

        missing = find_missing_assets(project_dir)
        assert "assets/nao_existe.png" in missing

    def test_detecta_multiplos_ausentes(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        write_manual_json(
            project_dir,
            _dados_com_prints("assets/a.png", "assets/b.png", "assets/c.png"),
        )

        missing = find_missing_assets(project_dir)
        assert len(missing) == 3

    def test_apenas_ausentes_sao_reportados(self, tmp_path):
        """Um presente + um ausente → só o ausente na lista."""
        project_dir = create_project_dir(tmp_path, "p")
        (project_dir / ASSETS_SUBDIR / "presente.png").write_bytes(_make_png_bytes())
        write_manual_json(
            project_dir,
            _dados_com_prints("assets/presente.png", "assets/ausente.png"),
        )

        missing = find_missing_assets(project_dir)
        assert missing == ["assets/ausente.png"]

    def test_retorna_lista_vazia_sem_prints(self, tmp_path):
        """Funcionalidade sem prints → lista vazia."""
        project_dir = create_project_dir(tmp_path, "p")
        dados = {
            "metadata": _META,
            "objetivo": "Obj.",
            "pre_requisito": "Nenhum.",
            "funcionalidades": [
                {"titulo": "F", "descricao": "D", "prints": [], "observacoes": []}
            ],
        }
        write_manual_json(project_dir, dados)
        assert find_missing_assets(project_dir) == []

    def test_retorna_lista_vazia_sem_manual_json(self, tmp_path):
        """Se manual.json não existe, retorna [] sem levantar exceção."""
        project_dir = create_project_dir(tmp_path, "p")
        assert find_missing_assets(project_dir) == []

    def test_retorna_lista_vazia_sem_funcionalidades(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        dados = {
            "metadata": _META,
            "objetivo": "Obj.",
            "pre_requisito": "Nenhum.",
            "funcionalidades": [],
        }
        write_manual_json(project_dir, dados)
        assert find_missing_assets(project_dir) == []


# ---------------------------------------------------------------------------
# Integração: import_project_zip + find_missing_assets
# ---------------------------------------------------------------------------

class TestImportComAssetsFaltando:
    def _zip_sem_assets(self) -> bytes:
        """Zip válido com manual.json referenciando assets/img.png, mas sem o arquivo."""
        dados = _dados_com_prints("assets/img.png")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr(MANUAL_JSON_NAME, json.dumps(dados, ensure_ascii=False))
        return buf.getvalue()

    def test_import_nao_levanta_excecao_por_assets_faltando(self, tmp_path):
        """Import bem-sucedido mesmo quando prints referenciados não estão no zip."""
        result = import_project_zip(self._zip_sem_assets(), tmp_path / "dest")
        assert result.exists()

    def test_find_missing_detecta_apos_import(self, tmp_path):
        """Após import sem assets, find_missing_assets reporta os paths ausentes."""
        dest = import_project_zip(self._zip_sem_assets(), tmp_path / "dest")
        missing = find_missing_assets(dest)
        assert "assets/img.png" in missing

    def test_find_missing_vazia_quando_assets_importados(self, tmp_path):
        """Quando zip inclui os assets, find_missing_assets retorna []."""
        dados = _dados_com_prints("assets/img.png")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr(MANUAL_JSON_NAME, json.dumps(dados, ensure_ascii=False))
            zf.writestr("assets/img.png", _make_png_bytes())
        dest = import_project_zip(buf.getvalue(), tmp_path / "dest")
        assert find_missing_assets(dest) == []
