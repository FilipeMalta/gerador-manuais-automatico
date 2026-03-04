"""
Trava o comportamento: prints em subpasta assets/ são incluídos no .docx.

Cenário: JSON com "prints": ["assets/print.png"] e o arquivo PNG existe
ao lado do JSON → docx gerado com tamanho > 0.
"""

import json
import pytest
from pathlib import Path
from PIL import Image

from src.gerador_manual import criar_manual


@pytest.fixture()
def manual_dir(tmp_path):
    """Monta um diretório temporário com manual.json e assets/print.png."""
    # Criar PNG mínimo válido em assets/
    assets_dir = tmp_path / "assets"
    assets_dir.mkdir()
    img = Image.new("RGB", (10, 10), color=(255, 0, 0))
    img.save(assets_dir / "print.png")

    # Criar manual.json referenciando o print em subpasta
    dados = {
        "metadata": {
            "nome_manual": "Manual Teste",
            "modulo": "Teste",
            "elaborado": "01/01/2025",
            "revisado": "01/01/2025",
            "classificacao": "interna",
        },
        "objetivo": "Testar geração com assets em subpasta.",
        "pre_requisito": "Nenhum.",
        "funcionalidades": [
            {
                "titulo": "Funcionalidade A",
                "descricao": "Descrição da funcionalidade A.",
                "prints": ["assets/print.png"],
                "observacoes": [],
            }
        ],
    }
    json_path = tmp_path / "manual.json"
    json_path.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")

    return tmp_path


def test_docx_gerado_com_print_em_subpasta(manual_dir):
    """docx é criado e tem tamanho > 0 quando o print está em assets/."""
    json_path = str(manual_dir / "manual.json")
    output_path = str(manual_dir / "output.docx")

    criar_manual(json_path, output_path)

    docx = Path(output_path)
    assert docx.exists(), "output.docx não foi criado"
    assert docx.stat().st_size > 0, "output.docx está vazio"


def test_docx_gerado_sem_prints(tmp_path):
    """docx é criado mesmo sem nenhum print."""
    dados = {
        "metadata": {
            "nome_manual": "Manual Sem Print",
            "modulo": "Sem Print",
            "elaborado": "01/01/2025",
            "revisado": "01/01/2025",
            "classificacao": "interna",
        },
        "objetivo": "Sem prints.",
        "pre_requisito": "Nenhum.",
        "funcionalidades": [
            {
                "titulo": "Funcionalidade B",
                "descricao": "Sem imagem.",
                "prints": [],
                "observacoes": [],
            }
        ],
    }
    json_path = tmp_path / "manual.json"
    json_path.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")

    output_path = str(tmp_path / "output.docx")
    criar_manual(str(json_path), output_path)

    docx = Path(output_path)
    assert docx.exists()
    assert docx.stat().st_size > 0
