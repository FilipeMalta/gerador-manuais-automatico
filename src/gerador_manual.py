"""
Gerador Automático de Manuais Word
Versão: 1.0.0
Autor: Filipe Malta Perfeito
"""

import json
import sys
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class GeradorManual:
    """Classe principal para geração de manuais Word"""
    
    def __init__(self, json_path: str, output_path: str):
        self.json_path = Path(json_path)
        self.output_path = Path(output_path)
        self.dados = self._carregar_json()
        self.doc = Document()
        
    def _carregar_json(self) -> dict:
        """Carrega e valida JSON de entrada"""
        if not self.json_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.json_path}")
        
        with open(self.json_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Validação básica
        campos_obrigatorios = ['metadata', 'objetivo', 'pre_requisito', 'funcionalidades']
        for campo in campos_obrigatorios:
            if campo not in dados:
                raise ValueError(f"Campo obrigatório ausente: {campo}")
        
        return dados
    
    def gerar(self):
        """Método principal de geração"""
        print("🚀 Iniciando geração do manual...")
        
        self._criar_capa()
        self.doc.add_page_break()
        
        self._criar_sumario()
        self.doc.add_page_break()
        
        self._criar_objetivo()
        self._criar_pre_requisito()
        self._criar_funcionalidades()
        
        self._aplicar_rodape()
        
        # Garantir que diretório de saída existe
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.doc.save(self.output_path)
        print(f"✅ Manual gerado com sucesso: {self.output_path}")
    
    def _criar_capa(self):
        """Cria capa padronizada"""
        metadata = self.dados['metadata']
        
        # Logo (se existir)
        logo_path = metadata.get('logo_path')
        if logo_path:
            logo_full_path = self.json_path.parent / logo_path
            if logo_full_path.exists():
                self.doc.add_picture(str(logo_full_path), width=Inches(2))
                self.doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Espaçamento
        for _ in range(5):
            self.doc.add_paragraph()
        
        # Título
        titulo = self.doc.add_heading(metadata['nome_manual'], level=1)
        titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = titulo.runs[0]
        run.font.size = Pt(24)
        run.font.bold = True
        
        # Módulo
        modulo = self.doc.add_paragraph(metadata['modulo'])
        modulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        modulo.runs[0].font.size = Pt(16)
        modulo.runs[0].font.color.rgb = RGBColor(100, 100, 100)
    
    def _criar_sumario(self):
        """Cria página de sumário"""
        heading = self.doc.add_heading('Sumário', level=1)
        
        # Adicionar campo de sumário automático
        paragraph = self.doc.add_paragraph()
        run = paragraph.add_run()
        
        # Instrução para atualização manual
        p_info = self.doc.add_paragraph()
        p_info.add_run('💡 Para atualizar o sumário: ').bold = True
        p_info.add_run('Clique com botão direito no sumário → "Atualizar campo"')
        p_info.runs[-1].font.size = Pt(9)
        p_info.runs[-1].font.color.rgb = RGBColor(150, 150, 150)
    
    def _criar_objetivo(self):
        """Cria seção de Objetivo"""
        self.doc.add_heading('1. Objetivo', level=1)
        self.doc.add_paragraph(self.dados['objetivo'])
        self.doc.add_paragraph()
    
    def _criar_pre_requisito(self):
        """Cria seção de Pré-requisito"""
        self.doc.add_heading('2. Pré-requisito', level=1)
        self.doc.add_paragraph(self.dados['pre_requisito'])
        self.doc.add_paragraph()
    
    def _criar_funcionalidades(self):
        """Cria seção de Funcionalidades"""
        self.doc.add_heading('3. Funcionalidade', level=1)
        
        for idx, func in enumerate(self.dados['funcionalidades'], start=1):
            # Subtítulo
            self.doc.add_heading(f'3.{idx} {func["titulo"]}', level=2)
            
            # Prints
            for print_nome in func.get('prints', []):
                print_path = self.json_path.parent / print_nome
                if print_path.exists():
                    try:
                        self.doc.add_picture(str(print_path), width=Inches(5.5))
                        last_paragraph = self.doc.paragraphs[-1]
                        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        self.doc.add_paragraph()  # Espaçamento
                    except Exception as e:
                        print(f"⚠️  Erro ao inserir imagem {print_nome}: {e}")
                        self.doc.add_paragraph(f'[Imagem não pode ser inserida: {print_nome}]')
                else:
                    print(f"⚠️  Imagem não encontrada: {print_path}")
                    self.doc.add_paragraph(f'[Imagem não encontrada: {print_nome}]')
            
            # Descrição
            self.doc.add_paragraph(func['descricao'])
            
            # Observações
            observacoes = func.get('observacoes', [])
            if observacoes:
                self.doc.add_paragraph()
                for obs_idx, obs_texto in enumerate(observacoes, start=1):
                    p = self.doc.add_paragraph()
                    p.add_run(f'Obs{obs_idx}: ').bold = True
                    p.add_run(obs_texto)
            
            self.doc.add_paragraph()
    
    def _aplicar_rodape(self):
        """Aplica rodapé padronizado"""
        metadata = self.dados['metadata']
        section = self.doc.sections[0]
        footer = section.footer
        
        # Limpar rodapé existente
        footer.paragraphs[0].clear()
        
        # Texto do rodapé
        footer_text = (
            f"Elaborado: {metadata['elaborado']} • "
            f"Revisado: {metadata['revisado']} • "
            f"Classificação: {metadata['classificacao']} • "
            f"Página "
        )
        
        p = footer.paragraphs[0]
        p.text = footer_text
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Número da página atual
        self._add_page_number(p)
        
        p.add_run(' de ')
        
        # Número total de páginas
        self._add_num_pages(p)
        
        # Estilo do rodapé
        run = p.runs[0]
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(100, 100, 100)
    
    def _add_page_number(self, paragraph):
        """Adiciona número de página atual"""
        run = paragraph.add_run()
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        
        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = "PAGE"
        
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')
        
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
    
    def _add_num_pages(self, paragraph):
        """Adiciona número total de páginas"""
        run = paragraph.add_run()
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        
        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = "NUMPAGES"
        
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')
        
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)


def main():
    """Função principal CLI"""
    if len(sys.argv) != 3:
        print("Uso: python gerador_manual.py <input.json> <output.docx>")
        print("\nExemplo:")
        print("  python gerador_manual.py exemplos/input/manual_input.json exemplos/output/Manual.docx")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        gerador = GeradorManual(json_path, output_path)
        gerador.gerar()
    except Exception as e:
        print(f"❌ Erro ao gerar manual: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
