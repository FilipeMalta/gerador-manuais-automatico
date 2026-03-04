"""
Trava o comportamento de export_project_zip:
- zip contém manual.json e assets/*
- conteúdo de cada entrada não está vazio
- arquivos avulsos na raiz também são incluídos
"""

import io
import json
import zipfile

import pytest

from src.projeto import ASSETS_SUBDIR, MANUAL_JSON_NAME, create_project_dir
from src.projeto_zip import export_project_zip


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def project_dir_com_assets(tmp_path):
    """project_dir com manual.json + 2 imagens em assets/."""
    project_dir = create_project_dir(tmp_path, "proj")

    dados = {
        "metadata": {
            "nome_manual": "Manual Zip",
            "modulo": "Zip",
            "elaborado": "01/01/2025",
            "revisado": "01/01/2025",
            "classificacao": "interna",
        },
        "objetivo": "Testar exportação zip.",
        "pre_requisito": "Nenhum.",
        "funcionalidades": [
            {
                "titulo": "F1",
                "descricao": "Descricao F1.",
                "prints": ["assets/img1.png", "assets/img2.png"],
                "observacoes": [],
            }
        ],
    }
    (project_dir / MANUAL_JSON_NAME).write_text(
        json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (project_dir / ASSETS_SUBDIR / "img1.png").write_bytes(b"\x89PNG img1")
    (project_dir / ASSETS_SUBDIR / "img2.png").write_bytes(b"\x89PNG img2")

    return project_dir


# ---------------------------------------------------------------------------
# Testes principais
# ---------------------------------------------------------------------------

class TestExportProjectZip:
    def test_retorna_bytes(self, project_dir_com_assets):
        result = export_project_zip(project_dir_com_assets)
        assert isinstance(result, bytes)

    def test_e_zip_valido(self, project_dir_com_assets):
        result = export_project_zip(project_dir_com_assets)
        assert zipfile.is_zipfile(io.BytesIO(result))

    def test_contem_manual_json(self, project_dir_com_assets):
        result = export_project_zip(project_dir_com_assets)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            assert MANUAL_JSON_NAME in zf.namelist()

    def test_contem_ambas_imagens(self, project_dir_com_assets):
        result = export_project_zip(project_dir_com_assets)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            names = zf.namelist()
            assert f"{ASSETS_SUBDIR}/img1.png" in names
            assert f"{ASSETS_SUBDIR}/img2.png" in names

    def test_entradas_nao_estao_vazias(self, project_dir_com_assets):
        result = export_project_zip(project_dir_com_assets)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            for name in zf.namelist():
                assert len(zf.read(name)) > 0, f"{name} está vazio no zip"

    def test_manual_json_conteudo_correto(self, project_dir_com_assets):
        result = export_project_zip(project_dir_com_assets)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            dados = json.loads(zf.read(MANUAL_JSON_NAME))
        assert dados["metadata"]["nome_manual"] == "Manual Zip"

    def test_separa_caminhos_com_barra(self, project_dir_com_assets):
        """Garante paths Unix (assets/x.png) mesmo rodando no Windows."""
        result = export_project_zip(project_dir_com_assets)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            for name in zf.namelist():
                assert "\\" not in name, f"Path com backslash no zip: {name}"


class TestExportZipComLogoAvulso:
    """Logo salvo na raiz do project_dir (fora de assets/) deve ser incluído."""

    def test_logo_avulso_incluido(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        (project_dir / MANUAL_JSON_NAME).write_text("{}", encoding="utf-8")
        (project_dir / "logo.png").write_bytes(b"logo-bytes")

        result = export_project_zip(project_dir)
        with zipfile.ZipFile(io.BytesIO(result)) as zf:
            assert "logo.png" in zf.namelist()
