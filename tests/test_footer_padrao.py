"""
Testes de rodapé corporativo no .docx gerado.
"""

import json
import re
import zipfile
from pathlib import Path

from src.gerador_manual import criar_manual


def _ler_xmls_footer(docx_path: Path) -> list[str]:
    """Retorna todo conteúdo de arquivos word/footer*.xml como texto."""
    with zipfile.ZipFile(docx_path) as docx_zip:
        footer_files = [
            name
            for name in docx_zip.namelist()
            if name.startswith('word/footer') and name.endswith('.xml')
        ]

        xmls = [docx_zip.read(name).decode('utf-8') for name in footer_files]
        return xmls


def test_footer_padrao_corporativo_com_fields_word(tmp_path):
    """Valida padrão textual do rodapé e fields PAGE/NUMPAGES."""
    dados = {
        'metadata': {
            'nome_manual': 'Manual de Teste de Rodapé',
            'modulo': 'Identificação de Músicas Gravadas',
            'elaborado': '04/03/2026',
            'revisado': '04/03/2026',
            'classificacao': 'interna',
        },
        'objetivo': 'Garantir que o rodapé siga o padrão corporativo obrigatório.',
        'pre_requisito': 'Ter acesso ao sistema e ao módulo correspondente.',
        'funcionalidades': [
            {
                'titulo': 'Funcionalidade de Exemplo',
                'descricao': 'Descrição mínima para gerar documento sem dependências externas.',
                'prints': [],
                'observacoes': [],
            }
        ],
    }

    json_path = tmp_path / 'manual.json'
    output_docx = tmp_path / 'manual.docx'
    json_path.write_text(json.dumps(dados, ensure_ascii=False), encoding='utf-8')

    criar_manual(str(json_path), str(output_docx))

    assert output_docx.exists(), 'Arquivo .docx não foi gerado'

    footer_xmls = _ler_xmls_footer(output_docx)
    assert footer_xmls, 'Nenhum arquivo word/footer*.xml encontrado no .docx'

    footer_xml = '\n'.join(footer_xmls)

    # Blocos textuais obrigatórios
    assert 'Elaborado:' in footer_xml
    assert ' por ' in footer_xml
    assert dados['metadata']['modulo'] in footer_xml
    assert 'Revisado:' in footer_xml
    assert 'Classificação:' in footer_xml
    assert 'Página' in footer_xml
    assert ' de ' in footer_xml

    # Campos automáticos do Word
    assert re.search(r'<w:instrText[^>]*>\s*PAGE\s*</w:instrText>', footer_xml)
    assert re.search(r'<w:instrText[^>]*>\s*NUMPAGES\s*</w:instrText>', footer_xml)


def test_footer_omite_por_quando_modulo_vazio(tmp_path):
    """Quando metadata.modulo está vazio, omite o trecho 'por ...'."""
    dados = {
        'metadata': {
            'nome_manual': 'Manual sem módulo',
            'modulo': '',
            'elaborado': '04/03/2026',
            'revisado': '04/03/2026',
            'classificacao': 'interna',
        },
        'objetivo': 'Objetivo suficiente para teste.',
        'pre_requisito': 'Pré-requisito suficiente para teste.',
        'funcionalidades': [
            {
                'titulo': 'Funcionalidade de Exemplo',
                'descricao': 'Descrição mínima para gerar documento sem dependências externas.',
                'prints': [],
                'observacoes': [],
            }
        ],
    }

    json_path = tmp_path / 'manual.json'
    output_docx = tmp_path / 'manual.docx'
    json_path.write_text(json.dumps(dados, ensure_ascii=False), encoding='utf-8')

    criar_manual(str(json_path), str(output_docx))

    footer_xmls = _ler_xmls_footer(output_docx)
    assert footer_xmls, 'Nenhum arquivo word/footer*.xml encontrado no .docx'

    footer_xml = '\n'.join(footer_xmls)
    assert 'Elaborado:' in footer_xml
    assert ' por ' not in footer_xml
