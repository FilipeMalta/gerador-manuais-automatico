"""
Trava que uploads persistem no workspace e o docx é gerado corretamente.

Cobre dois critérios:
1. save_uploaded_file grava em disco e retorna caminho relativo (já coberto
   em test_projeto_workspace.py, repetido aqui como contrato explícito).
2. Integração completa: save_uploaded_file → write_manual_json → criar_manual
   → docx existe e tem tamanho > 0 (imagem entra no documento).
"""

import json
import pytest
from pathlib import Path
from PIL import Image

from src.gerador_manual import criar_manual
from src.projeto import (
    ASSETS_SUBDIR,
    create_project_dir,
    save_uploaded_file,
    write_manual_json,
)


# ---------------------------------------------------------------------------
# Stub de UploadedFile (sem Streamlit)
# ---------------------------------------------------------------------------

class FakeUploadedFile:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self._content = content

    def read(self) -> bytes:
        return self._content


def _make_png(tmp_path: Path, name: str = "screen.png") -> FakeUploadedFile:
    """Cria um PNG mínimo em memória usando Pillow."""
    img = Image.new("RGB", (20, 20), color=(0, 128, 255))
    buf_path = tmp_path / name
    img.save(buf_path)
    return FakeUploadedFile(name, buf_path.read_bytes())


# ---------------------------------------------------------------------------
# 1. Contrato de persistência de uploads
# ---------------------------------------------------------------------------

class TestSaveUploadedFilePersists:
    def test_arquivo_existe_em_disco(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        fake = _make_png(tmp_path, "img.png")
        rel = save_uploaded_file(project_dir, fake, kind="print")
        assert (project_dir / rel).exists()

    def test_conteudo_identico_ao_upload(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        fake = _make_png(tmp_path, "img.png")
        original_bytes = fake.read()

        # Reinicia o conteúdo (read() consome o buffer de FakeUploadedFile)
        fake2 = FakeUploadedFile("img.png", original_bytes)
        rel = save_uploaded_file(project_dir, fake2)
        assert (project_dir / rel).read_bytes() == original_bytes

    def test_caminho_relativo_usa_assets(self, tmp_path):
        project_dir = create_project_dir(tmp_path, "p")
        fake = _make_png(tmp_path, "screenshot.png")
        rel = save_uploaded_file(project_dir, fake)
        assert rel == f"{ASSETS_SUBDIR}/screenshot.png"


# ---------------------------------------------------------------------------
# 2. Integração: save_uploaded_file → write_manual_json → criar_manual
# ---------------------------------------------------------------------------

class TestIntegracaoWorkspaceDocx:
    def test_docx_gerado_com_print_persistido(self, tmp_path):
        """
        Fluxo completo:
          1. Criar workspace
          2. Persistir print via save_uploaded_file
          3. Escrever manual.json com caminho assets/...
          4. Gerar docx com criar_manual
          5. Validar docx existe e tem tamanho > 0
        """
        project_dir = create_project_dir(tmp_path, "proj")

        # Simula upload
        fake = _make_png(tmp_path, "tela.png")
        rel_path = save_uploaded_file(project_dir, fake, kind="print")

        # Monta manual.json com o caminho persistido
        dados = {
            "metadata": {
                "nome_manual": "Manual Integração",
                "modulo": "Módulo Teste",
                "elaborado": "01/01/2025",
                "revisado": "01/01/2025",
                "classificacao": "interna",
            },
            "objetivo": "Testar integração completa do fluxo de upload.",
            "pre_requisito": "Nenhum pré-requisito.",
            "funcionalidades": [
                {
                    "titulo": "Funcionalidade com Print",
                    "descricao": "Descrição da funcionalidade com imagem.",
                    "prints": [rel_path],
                    "observacoes": [],
                }
            ],
        }
        json_path = write_manual_json(project_dir, dados)

        output_path = tmp_path / "Manual_Integracao.docx"
        criar_manual(str(json_path), str(output_path))

        assert output_path.exists(), "docx não foi criado"
        assert output_path.stat().st_size > 0, "docx está vazio"

    def test_docx_gerado_com_multiplos_prints(self, tmp_path):
        """Dois prints persistidos → docx gerado sem erro."""
        project_dir = create_project_dir(tmp_path, "proj")

        rel1 = save_uploaded_file(project_dir, _make_png(tmp_path, "p1.png"))
        rel2 = save_uploaded_file(project_dir, _make_png(tmp_path, "p2.png"))

        dados = {
            "metadata": {
                "nome_manual": "Manual Multi-Print",
                "modulo": "Multi",
                "elaborado": "01/01/2025",
                "revisado": "01/01/2025",
                "classificacao": "interna",
            },
            "objetivo": "Testar múltiplos prints persistidos.",
            "pre_requisito": "Nenhum.",
            "funcionalidades": [
                {
                    "titulo": "Func",
                    "descricao": "Com dois prints.",
                    "prints": [rel1, rel2],
                    "observacoes": [],
                }
            ],
        }
        json_path = write_manual_json(project_dir, dados)
        output_path = tmp_path / "out.docx"
        criar_manual(str(json_path), str(output_path))

        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_print_ausente_nao_quebra_geracao(self, tmp_path):
        """Se o arquivo de imagem não existir, criar_manual não deve lançar exceção
        (registra aviso e continua)."""
        project_dir = create_project_dir(tmp_path, "proj")

        dados = {
            "metadata": {
                "nome_manual": "Manual Sem Imagem Real",
                "modulo": "Sem Img",
                "elaborado": "01/01/2025",
                "revisado": "01/01/2025",
                "classificacao": "interna",
            },
            "objetivo": "Testar que imagem ausente não quebra o gerador.",
            "pre_requisito": "Nenhum.",
            "funcionalidades": [
                {
                    "titulo": "Func",
                    "descricao": "Print referenciado mas arquivo não existe.",
                    "prints": ["assets/nao_existe.png"],
                    "observacoes": [],
                }
            ],
        }
        json_path = write_manual_json(project_dir, dados)
        output_path = tmp_path / "out.docx"

        # Não deve levantar exceção — gerador trata imagens ausentes com try/except
        criar_manual(str(json_path), str(output_path))
        assert output_path.exists()
