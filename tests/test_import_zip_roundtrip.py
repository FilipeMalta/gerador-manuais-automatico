"""
Trava o round-trip export → import:
- JSON importado é idêntico ao original
- Arquivos assets/ são restaurados com o mesmo conteúdo
- Erros de segurança são detectados (path traversal, zip sem manual.json)
"""

import io
import json
import zipfile

import pytest
from pathlib import Path

from src.projeto import ASSETS_SUBDIR, MANUAL_JSON_NAME, create_project_dir
from src.projeto_zip import export_project_zip, import_project_zip


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

DADOS_ORIGINAL = {
    "metadata": {
        "nome_manual": "Roundtrip Manual",
        "modulo": "Módulo RT",
        "sistema": "Sistema X",
        "elaborado": "01/03/2025",
        "revisado": "02/03/2025",
        "classificacao": "interna",
    },
    "objetivo": "Testar round-trip completo de exportação e importação.",
    "pre_requisito": "Nenhum pré-requisito.",
    "funcionalidades": [
        {
            "titulo": "Funcionalidade A",
            "descricao": "Descrição da funcionalidade A.",
            "prints": ["assets/img1.png", "assets/img2.png"],
            "observacoes": ["Obs 1 da func A."],
        }
    ],
}

IMG1_BYTES = b"\x89PNG\r\n\x1a\n img1 content"
IMG2_BYTES = b"\x89PNG\r\n\x1a\n img2 content"


@pytest.fixture()
def projeto_exportado(tmp_path):
    """Cria project_dir com manual.json + 2 imagens e retorna (project_dir, zip_bytes)."""
    project_dir = create_project_dir(tmp_path / "origem", "proj")

    (project_dir / MANUAL_JSON_NAME).write_text(
        json.dumps(DADOS_ORIGINAL, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (project_dir / ASSETS_SUBDIR / "img1.png").write_bytes(IMG1_BYTES)
    (project_dir / ASSETS_SUBDIR / "img2.png").write_bytes(IMG2_BYTES)

    zip_bytes = export_project_zip(project_dir)
    return project_dir, zip_bytes


# ---------------------------------------------------------------------------
# Round-trip: estrutura de diretórios
# ---------------------------------------------------------------------------

class TestImportEstrutura:
    def test_retorna_path(self, projeto_exportado, tmp_path):
        _, zip_bytes = projeto_exportado
        result = import_project_zip(zip_bytes, tmp_path / "dest")
        assert isinstance(result, Path)

    def test_manual_json_extraido(self, projeto_exportado, tmp_path):
        _, zip_bytes = projeto_exportado
        dest = import_project_zip(zip_bytes, tmp_path / "dest")
        assert (dest / MANUAL_JSON_NAME).exists()

    def test_assets_extraidos(self, projeto_exportado, tmp_path):
        _, zip_bytes = projeto_exportado
        dest = import_project_zip(zip_bytes, tmp_path / "dest")
        assert (dest / ASSETS_SUBDIR / "img1.png").exists()
        assert (dest / ASSETS_SUBDIR / "img2.png").exists()

    def test_cria_dest_dir_se_nao_existe(self, projeto_exportado, tmp_path):
        _, zip_bytes = projeto_exportado
        dest = tmp_path / "novo" / "dest"
        assert not dest.exists()
        import_project_zip(zip_bytes, dest)
        assert dest.exists()


# ---------------------------------------------------------------------------
# Round-trip: conteúdo idêntico ao original
# ---------------------------------------------------------------------------

class TestImportConteudo:
    def test_json_identico_ao_original(self, projeto_exportado, tmp_path):
        _, zip_bytes = projeto_exportado
        dest = import_project_zip(zip_bytes, tmp_path / "dest")
        importado = json.loads((dest / MANUAL_JSON_NAME).read_text(encoding="utf-8"))
        assert importado == DADOS_ORIGINAL

    def test_bytes_img1_identicos(self, projeto_exportado, tmp_path):
        _, zip_bytes = projeto_exportado
        dest = import_project_zip(zip_bytes, tmp_path / "dest")
        assert (dest / ASSETS_SUBDIR / "img1.png").read_bytes() == IMG1_BYTES

    def test_bytes_img2_identicos(self, projeto_exportado, tmp_path):
        _, zip_bytes = projeto_exportado
        dest = import_project_zip(zip_bytes, tmp_path / "dest")
        assert (dest / ASSETS_SUBDIR / "img2.png").read_bytes() == IMG2_BYTES

    def test_metadados_preservados(self, projeto_exportado, tmp_path):
        _, zip_bytes = projeto_exportado
        dest = import_project_zip(zip_bytes, tmp_path / "dest")
        dados = json.loads((dest / MANUAL_JSON_NAME).read_text(encoding="utf-8"))
        assert dados["metadata"]["nome_manual"] == "Roundtrip Manual"
        assert dados["metadata"]["modulo"] == "Módulo RT"
        assert dados["metadata"]["classificacao"] == "interna"

    def test_funcionalidades_preservadas(self, projeto_exportado, tmp_path):
        _, zip_bytes = projeto_exportado
        dest = import_project_zip(zip_bytes, tmp_path / "dest")
        dados = json.loads((dest / MANUAL_JSON_NAME).read_text(encoding="utf-8"))
        assert len(dados["funcionalidades"]) == 1
        func = dados["funcionalidades"][0]
        assert func["titulo"] == "Funcionalidade A"
        assert "assets/img1.png" in func["prints"]


# ---------------------------------------------------------------------------
# Segurança
# ---------------------------------------------------------------------------

class TestImportSeguranca:
    def test_rejeita_zip_sem_manual_json(self, tmp_path):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("assets/img.png", b"data")
        with pytest.raises(ValueError, match="manual.json"):
            import_project_zip(buf.getvalue(), tmp_path / "dest")

    def test_rejeita_bytes_invalidos(self, tmp_path):
        with pytest.raises(ValueError, match="zip válido"):
            import_project_zip(b"not a zip", tmp_path / "dest")

    def test_rejeita_path_traversal(self, tmp_path):
        schema_valido = json.dumps({
            "metadata": {
                "nome_manual": "X", "modulo": "X",
                "elaborado": "01/01/2025", "revisado": "01/01/2025",
                "classificacao": "interna",
            },
            "funcionalidades": [],
        })
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("manual.json", schema_valido)
            zf.writestr("../../evil.txt", "pwned")
        with pytest.raises(ValueError, match="[Pp]ath traversal"):
            import_project_zip(buf.getvalue(), tmp_path / "dest")
