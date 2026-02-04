"""
Gerador Automático de Manuais Word
Baseado no padrão corporativo definido
Versão: 1.0.0
"""

import json
import sys
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn


def criar_manual(json_path: str, output_path: str):
    """
    Gera manual .docx a partir de JSON estruturado
    
    Args:
        json_path: Caminho do JSON com conteúdo
        output_path: Caminho de saída do .docx
    """
    
    # Carregar dados
    with open(json_path, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # Criar documento
    doc = Document()
    
    # ===== CAPA =====
    criar_capa(doc, dados['metadata'], json_path)
    doc.add_page_break()
    
    # ===== SUMÁRIO =====
    criar_sumario(doc)
    doc.add_page_break()
    
    # ===== OBJETIVO =====
    doc.add_heading('1. Objetivo', level=1)
    doc.add_paragraph(dados['objetivo'])
    doc.add_paragraph()
    
    # ===== PRÉ-REQUISITO =====
    doc.add_heading('2. Pré-requisito', level=1)
    doc.add_paragraph(dados['pre_requisito'])
    doc.add_paragraph()
    
    # ===== FUNCIONALIDADES =====
    doc.add_heading('3. Funcionalidade', level=1)
    
    for idx, func in enumerate(dados['funcionalidades'], start=1):
        # Título da funcionalidade
        doc.add_heading(f'3.{idx} {func["titulo"]}', level=2)
        
        # Prints (se houver)
        json_dir = Path(json_path).parent
        for print_path in func.get('prints', []):
            full_path = json_dir / print_path
            try:
                doc.add_picture(str(full_path), width=Inches(5.5))
                last_paragraph = doc.paragraphs[-1]
                last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                doc.add_paragraph()  # Espaçamento
            except Exception as e:
                print(f"[AVISO] Erro ao inserir imagem {print_path}: {e}")
                doc.add_paragraph(f'[Imagem não encontrada: {print_path}]')
        
        # Descrição
        doc.add_paragraph(func['descricao'])
        
        # Observações
        if func.get('observacoes'):
            doc.add_paragraph()
            for obs_idx, obs in enumerate(func['observacoes'], start=1):
                p = doc.add_paragraph()
                p.add_run(f'Obs{obs_idx}: ').bold = True
                p.add_run(obs)
        
        doc.add_paragraph()
    
    # ===== RODAPÉ =====
    aplicar_rodape(doc, dados['metadata'])
    
    # Garantir diretório de saída
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Salvar
    doc.save(output_path)
    print(f'[OK] Manual gerado com sucesso: {output_path}')


def criar_capa(doc, metadata, json_path):
    """Cria capa padronizada"""
    
    # Logo (se existir)
    if metadata.get('logo_path'):
        json_dir = Path(json_path).parent
        logo_full_path = json_dir / metadata['logo_path']
        try:
            doc.add_picture(str(logo_full_path), width=Inches(2))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        except Exception as e:
            print(f"[AVISO] Logo nao encontrada: {e}")
    
    # Espaçamento
    for _ in range(5):
        doc.add_paragraph()
    
    # Título
    titulo = doc.add_heading(metadata['nome_manual'], level=1)
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    titulo.runs[0].font.size = Pt(24)
    titulo.runs[0].font.bold = True
    
    # Módulo
    modulo = doc.add_paragraph(metadata['modulo'])
    modulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    modulo.runs[0].font.size = Pt(16)
    modulo.runs[0].font.color.rgb = RGBColor(128, 128, 128)


def criar_sumario(doc):
    """Cria página de sumário com campo TOC do Word"""
    doc.add_heading('Sumário', level=1)

    # Criar campo TOC (Table of Contents) do Word
    paragraph = doc.add_paragraph()
    run = paragraph.add_run()

    # Início do campo
    fldChar1 = run._element.makeelement(qn('w:fldChar'))
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._element.append(fldChar1)

    # Instrução do campo TOC
    instrText = run._element.makeelement(qn('w:instrText'))
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'TOC \\o "1-2" \\h \\z \\u'
    run._element.append(instrText)

    # Separador
    fldChar2 = run._element.makeelement(qn('w:fldChar'))
    fldChar2.set(qn('w:fldCharType'), 'separate')
    run._element.append(fldChar2)

    # Texto placeholder
    run2 = paragraph.add_run('Clique com botao direito e selecione "Atualizar campo" para gerar o sumario')
    run2.font.italic = True
    run2.font.color.rgb = RGBColor(150, 150, 150)

    # Fim do campo
    run3 = paragraph.add_run()
    fldChar3 = run3._element.makeelement(qn('w:fldChar'))
    fldChar3.set(qn('w:fldCharType'), 'end')
    run3._element.append(fldChar3)


def aplicar_rodape(doc, metadata):
    """Aplica rodapé padronizado em todas as páginas"""
    section = doc.sections[0]
    footer = section.footer
    
    footer_text = (
        f"Elaborado: {metadata['elaborado']} • "
        f"Revisado: {metadata['revisado']} • "
        f"Classificação: {metadata['classificacao']} • "
        f"Página "
    )
    
    p = footer.paragraphs[0]
    p.text = footer_text
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].font.size = Pt(9)
    p.runs[0].font.color.rgb = RGBColor(100, 100, 100)
    
    # Adicionar número de página atual
    run = p.add_run()
    fldChar1 = run._element.makeelement(qn('w:fldChar'))
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._element.append(fldChar1)
    
    instrText = run._element.makeelement(qn('w:instrText'))
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    run._element.append(instrText)
    
    fldChar2 = run._element.makeelement(qn('w:fldChar'))
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._element.append(fldChar2)
    
    p.add_run(' de ')
    
    # Adicionar número total de páginas
    run = p.add_run()
    fldChar1 = run._element.makeelement(qn('w:fldChar'))
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._element.append(fldChar1)
    
    instrText = run._element.makeelement(qn('w:instrText'))
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "NUMPAGES"
    run._element.append(instrText)
    
    fldChar2 = run._element.makeelement(qn('w:fldChar'))
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._element.append(fldChar2)


def main():
    """Interface CLI"""
    if len(sys.argv) != 3:
        print("Uso: python gerador_manual.py <input.json> <output.docx>")
        print("\nExemplo:")
        print("  python gerador_manual.py exemplos/input/manual_input.json exemplos/output/Manual.docx")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        criar_manual(json_path, output_path)
    except FileNotFoundError as e:
        print(f"[ERRO] {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"[ERRO] JSON invalido em {json_path}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERRO] Ao gerar manual: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
