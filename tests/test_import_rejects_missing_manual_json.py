"""
Trava que import_project_zip rejeita zips com manual.json inválido ou ausente.

Cobre:
1. Zip sem manual.json (já coberto em test_import_zip_roundtrip, repetido
   aqui como contrato explícito de rejeição).
2. manual.json com JSON inválido (não parseável).
3. Schema mínimo: chaves obrigatórias de topo (metadata, funcionalidades).
4. Schema mínimo: chaves obrigatórias de metadata (nome_manual, modulo, etc.).
5. Tipo incorreto: funcionalidades não é lista.
"""

import io
import json
import zipfile

import pytest

from src.projeto_zip import import_project_zip

# ---------------------------------------------------------------------------
# Helper para montar um zip mínimo em memória
# ---------------------------------------------------------------------------

_SCHEMA_VALIDO = {
    "metadata": {
        "nome_manual": "Manual Teste",
        "modulo": "Módulo X",
        "elaborado": "01/01/2025",
        "revisado": "01/01/2025",
        "classificacao": "interna",
    },
    "objetivo": "Objetivo.",
    "pre_requisito": "Nenhum.",
    "funcionalidades": [],
}


def _make_zip(entries: dict[str, str | bytes]) -> bytes:
    """Cria zip in-memory. Valores str → UTF-8; bytes → raw."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, content in entries.items():
            if isinstance(content, str):
                zf.writestr(name, content.encode("utf-8"))
            else:
                zf.writestr(name, content)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# 1. Ausência de manual.json
# ---------------------------------------------------------------------------

class TestRejeicaoAusenciaManualJson:
    def test_rejeita_zip_sem_manual_json(self, tmp_path):
        zip_bytes = _make_zip({"assets/img.png": b"data"})
        with pytest.raises(ValueError, match="manual.json"):
            import_project_zip(zip_bytes, tmp_path / "dest")


# ---------------------------------------------------------------------------
# 2. manual.json com JSON inválido
# ---------------------------------------------------------------------------

class TestRejeicaoJsonInvalido:
    def test_rejeita_json_mal_formado(self, tmp_path):
        zip_bytes = _make_zip({"manual.json": b"{chave sem aspas: valor}"})
        with pytest.raises(ValueError, match="JSON válido"):
            import_project_zip(zip_bytes, tmp_path / "dest")

    def test_rejeita_json_vazio(self, tmp_path):
        zip_bytes = _make_zip({"manual.json": b""})
        with pytest.raises(ValueError, match="JSON válido"):
            import_project_zip(zip_bytes, tmp_path / "dest")

    def test_rejeita_json_array_raiz(self, tmp_path):
        """JSON válido mas não é objeto (dict) — schema deve rejeitar."""
        zip_bytes = _make_zip({"manual.json": json.dumps([1, 2, 3])})
        with pytest.raises(ValueError):
            import_project_zip(zip_bytes, tmp_path / "dest")


# ---------------------------------------------------------------------------
# 3. Schema: chaves obrigatórias de topo
# ---------------------------------------------------------------------------

class TestRejeicaoSchemaTopo:
    def test_rejeita_sem_metadata(self, tmp_path):
        dados = {k: v for k, v in _SCHEMA_VALIDO.items() if k != "metadata"}
        zip_bytes = _make_zip({"manual.json": json.dumps(dados)})
        with pytest.raises(ValueError, match="metadata"):
            import_project_zip(zip_bytes, tmp_path / "dest")

    def test_rejeita_sem_funcionalidades(self, tmp_path):
        dados = {k: v for k, v in _SCHEMA_VALIDO.items() if k != "funcionalidades"}
        zip_bytes = _make_zip({"manual.json": json.dumps(dados)})
        with pytest.raises(ValueError, match="funcionalidades"):
            import_project_zip(zip_bytes, tmp_path / "dest")


# ---------------------------------------------------------------------------
# 4. Schema: chaves obrigatórias de metadata
# ---------------------------------------------------------------------------

class TestRejeicaoSchemaMetadata:
    @pytest.mark.parametrize("chave_ausente", [
        "nome_manual", "modulo", "elaborado", "revisado", "classificacao"
    ])
    def test_rejeita_metadata_sem_chave(self, tmp_path, chave_ausente):
        dados = json.loads(json.dumps(_SCHEMA_VALIDO))  # deep copy
        del dados["metadata"][chave_ausente]
        zip_bytes = _make_zip({"manual.json": json.dumps(dados)})
        with pytest.raises(ValueError, match="metadata"):
            import_project_zip(zip_bytes, tmp_path / "dest")


# ---------------------------------------------------------------------------
# 5. Tipo incorreto: funcionalidades não é lista
# ---------------------------------------------------------------------------

class TestRejeicaoTipoIncorreto:
    def test_rejeita_funcionalidades_objeto(self, tmp_path):
        dados = json.loads(json.dumps(_SCHEMA_VALIDO))
        dados["funcionalidades"] = {"chave": "valor"}
        zip_bytes = _make_zip({"manual.json": json.dumps(dados)})
        with pytest.raises(ValueError, match="funcionalidades"):
            import_project_zip(zip_bytes, tmp_path / "dest")

    def test_rejeita_funcionalidades_string(self, tmp_path):
        dados = json.loads(json.dumps(_SCHEMA_VALIDO))
        dados["funcionalidades"] = "não é lista"
        zip_bytes = _make_zip({"manual.json": json.dumps(dados)})
        with pytest.raises(ValueError, match="funcionalidades"):
            import_project_zip(zip_bytes, tmp_path / "dest")


# ---------------------------------------------------------------------------
# 6. Schema válido é aceito
# ---------------------------------------------------------------------------

class TestSchemaValidoAceito:
    def test_schema_valido_nao_levanta_excecao(self, tmp_path):
        zip_bytes = _make_zip({"manual.json": json.dumps(_SCHEMA_VALIDO)})
        result = import_project_zip(zip_bytes, tmp_path / "dest")
        assert result.exists()
