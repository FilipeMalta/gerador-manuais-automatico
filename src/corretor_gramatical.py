"""
Corretor Gramatical em Português Brasileiro
Versão Leve: Baseada em padrões e dicionário de erros comuns
Versão: 2.0.0 (Sem dependências pesadas)
"""

import re
import json
from typing import List, Dict, Tuple, Optional
from pathlib import Path


# Dicionário de erros comuns em PT-BR com sugestões
ERROS_COMUNS = {
    # Acentuação (80+ palavras)
    'usuario': {'sugestoes': ['usuário'], 'tipo': 'acentuacao'},
    'modulo': {'sugestoes': ['módulo'], 'tipo': 'acentuacao'},
    'funcao': {'sugestoes': ['função'], 'tipo': 'acentuacao'},
    'acao': {'sugestoes': ['ação'], 'tipo': 'acentuacao'},
    'dados': {'sugestoes': ['dados'], 'tipo': 'acentuacao'},
    'metodo': {'sugestoes': ['método'], 'tipo': 'acentuacao'},
    'generico': {'sugestoes': ['genérico'], 'tipo': 'acentuacao'},
    'critico': {'sugestoes': ['crítico'], 'tipo': 'acentuacao'},
    'otografia': {'sugestoes': ['ortografia'], 'tipo': 'acentuacao'},
    'senario': {'sugestoes': ['cenário'], 'tipo': 'acentuacao'},
    'inclusao': {'sugestoes': ['inclusão'], 'tipo': 'acentuacao'},
    'calcao': {'sugestoes': ['calção'], 'tipo': 'acentuacao'},
    'seleçao': {'sugestoes': ['seleção'], 'tipo': 'acentuacao'},
    'verificaçao': {'sugestoes': ['verificação'], 'tipo': 'acentuacao'},
    'operaçao': {'sugestoes': ['operação'], 'tipo': 'acentuacao'},
    'configuraçao': {'sugestoes': ['configuração'], 'tipo': 'acentuacao'},
    'situaçao': {'sugestoes': ['situação'], 'tipo': 'acentuacao'},
    'informaçao': {'sugestoes': ['informação'], 'tipo': 'acentuacao'},
    'comunicaçao': {'sugestoes': ['comunicação'], 'tipo': 'acentuacao'},
    'soluçao': {'sugestoes': ['solução'], 'tipo': 'acentuacao'},
    'posiçao': {'sugestoes': ['posição'], 'tipo': 'acentuacao'},
    'direcçao': {'sugestoes': ['direção'], 'tipo': 'acentuacao'},
    'intencao': {'sugestoes': ['intenção'], 'tipo': 'acentuacao'},
    'atençao': {'sugestoes': ['atenção'], 'tipo': 'acentuacao'},
    'paixao': {'sugestoes': ['paixão'], 'tipo': 'acentuacao'},
    'manutencao': {'sugestoes': ['manutenção'], 'tipo': 'acentuacao'},
    'protecao': {'sugestoes': ['proteção'], 'tipo': 'acentuacao'},
    'retencao': {'sugestoes': ['retenção'], 'tipo': 'acentuacao'},
    'extensao': {'sugestoes': ['extensão'], 'tipo': 'acentuacao'},
    'supervisao': {'sugestoes': ['supervisão'], 'tipo': 'acentuacao'},
    'conclusao': {'sugestoes': ['conclusão'], 'tipo': 'acentuacao'},
    'propulsao': {'sugestoes': ['propulsão'], 'tipo': 'acentuacao'},
    'discussao': {'sugestoes': ['discussão'], 'tipo': 'acentuacao'},
    'sessao': {'sugestoes': ['sessão'], 'tipo': 'acentuacao'},
    'expressao': {'sugestoes': ['expressão'], 'tipo': 'acentuacao'},
    'compressao': {'sugestoes': ['compressão'], 'tipo': 'acentuacao'},
    'impressao': {'sugestoes': ['impressão'], 'tipo': 'acentuacao'},
    'diversao': {'sugestoes': ['diversão'], 'tipo': 'acentuacao'},
    'aventura': {'sugestoes': ['aventura'], 'tipo': 'acentuacao'},
    'loucura': {'sugestoes': ['loucura'], 'tipo': 'acentuacao'},
    'ternura': {'sugestoes': ['ternura'], 'tipo': 'acentuacao'},
    'criacao': {'sugestoes': ['criação'], 'tipo': 'acentuacao'},
    'educacao': {'sugestoes': ['educação'], 'tipo': 'acentuacao'},
    'producao': {'sugestoes': ['produção'], 'tipo': 'acentuacao'},
    'reducao': {'sugestoes': ['redução'], 'tipo': 'acentuacao'},
    'traducao': {'sugestoes': ['tradução'], 'tipo': 'acentuacao'},
    'construcao': {'sugestoes': ['construção'], 'tipo': 'acentuacao'},
    'destrucao': {'sugestoes': ['destruição'], 'tipo': 'acentuacao'},
    'obtencao': {'sugestoes': ['obtenção'], 'tipo': 'acentuacao'},
    'sustentacao': {'sugestoes': ['sustentação'], 'tipo': 'acentuacao'},
    'apresentacao': {'sugestoes': ['apresentação'], 'tipo': 'acentuacao'},
    'representacao': {'sugestoes': ['representação'], 'tipo': 'acentuacao'},
    'abreviacao': {'sugestoes': ['abreviação'], 'tipo': 'acentuacao'},
    'remuneracao': {'sugestoes': ['remuneração'], 'tipo': 'acentuacao'},
    'recomendacao': {'sugestoes': ['recomendação'], 'tipo': 'acentuacao'},
    'demarcacao': {'sugestoes': ['demarcação'], 'tipo': 'acentuacao'},
    'dedicacao': {'sugestoes': ['dedicação'], 'tipo': 'acentuacao'},
    'mediacacao': {'sugestoes': ['medicação'], 'tipo': 'acentuacao'},
    'predicacao': {'sugestoes': ['predicação'], 'tipo': 'acentuacao'},
    'radicacao': {'sugestoes': ['radicação'], 'tipo': 'acentuacao'},
    'aviacao': {'sugestoes': ['aviação'], 'tipo': 'acentuacao'},
    'vacinacao': {'sugestoes': ['vacinação'], 'tipo': 'acentuacao'},
    'nulacao': {'sugestoes': ['anulação'], 'tipo': 'acentuacao'},
    'regulacao': {'sugestoes': ['regulação'], 'tipo': 'acentuacao'},
    'simulacao': {'sugestoes': ['simulação'], 'tipo': 'acentuacao'},
    'emulacao': {'sugestoes': ['emulação'], 'tipo': 'acentuacao'},
    'enumeracao': {'sugestoes': ['enumeração'], 'tipo': 'acentuacao'},
    'separacao': {'sugestoes': ['separação'], 'tipo': 'acentuacao'},
    'preparacao': {'sugestoes': ['preparação'], 'tipo': 'acentuacao'},
    'reparacao': {'sugestoes': ['reparação'], 'tipo': 'acentuacao'},
    'comparacao': {'sugestoes': ['comparação'], 'tipo': 'acentuacao'},
    'declaracao': {'sugestoes': ['declaração'], 'tipo': 'acentuacao'},
    'inflamacao': {'sugestoes': ['inflamação'], 'tipo': 'acentuacao'},
    'examinacao': {'sugestoes': ['examinação'], 'tipo': 'acentuacao'},
    'continuacao': {'sugestoes': ['continuação'], 'tipo': 'acentuacao'},
    'pulsacao': {'sugestoes': ['pulsação'], 'tipo': 'acentuacao'},
    'rotacao': {'sugestoes': ['rotação'], 'tipo': 'acentuacao'},
    'notacao': {'sugestoes': ['notação'], 'tipo': 'acentuacao'},
    'quotacao': {'sugestoes': ['cotação'], 'tipo': 'acentuacao'},
    'flutuacao': {'sugestoes': ['flutuação'], 'tipo': 'acentuacao'},
    
    # Ortografia comum (80+)
    'proceso': {'sugestoes': ['processo'], 'tipo': 'ortografia'},
    'recesso': {'sugestoes': ['recesso', 'processo'], 'tipo': 'ortografia'},
    'sisitema': {'sugestoes': ['sistema'], 'tipo': 'ortografia'},
    'exessivo': {'sugestoes': ['excessivo'], 'tipo': 'ortografia'},
    'acessivel': {'sugestoes': ['acessível'], 'tipo': 'ortografia'},
    'sensivel': {'sugestoes': ['sensível'], 'tipo': 'ortografia'},
    'possivel': {'sugestoes': ['possível'], 'tipo': 'ortografia'},
    'responsavel': {'sugestoes': ['responsável'], 'tipo': 'ortografia'},
    'razoavel': {'sugestoes': ['razoável'], 'tipo': 'ortografia'},
    'favoravel': {'sugestoes': ['favorável'], 'tipo': 'ortografia'},
    'compativel': {'sugestoes': ['compatível'], 'tipo': 'ortografia'},
    'confortavel': {'sugestoes': ['confortável'], 'tipo': 'ortografia'},
    'desconfortavel': {'sugestoes': ['desconfortável'], 'tipo': 'ortografia'},
    'suportavel': {'sugestoes': ['suportável'], 'tipo': 'ortografia'},
    'preferivel': {'sugestoes': ['preferível'], 'tipo': 'ortografia'},
    'irreversivel': {'sugestoes': ['irreversível'], 'tipo': 'ortografia'},
    'reversivel': {'sugestoes': ['reversível'], 'tipo': 'ortografia'},
    'inadmissivel': {'sugestoes': ['inadmissível'], 'tipo': 'ortografia'},
    'admissivel': {'sugestoes': ['admissível'], 'tipo': 'ortografia'},
    'permissivel': {'sugestoes': ['permissível'], 'tipo': 'ortografia'},
    'exequivel': {'sugestoes': ['exequível'], 'tipo': 'ortografia'},
    'execivel': {'sugestoes': ['executável'], 'tipo': 'ortografia'},
    'acessorio': {'sugestoes': ['acessório'], 'tipo': 'ortografia'},
    'subsidiario': {'sugestoes': ['subsidiário'], 'tipo': 'ortografia'},
    'ordinario': {'sugestoes': ['ordinário'], 'tipo': 'ortografia'},
    'salario': {'sugestoes': ['salário'], 'tipo': 'ortografia'},
    'beneficiario': {'sugestoes': ['beneficiário'], 'tipo': 'ortografia'},
    'inventario': {'sugestoes': ['inventário'], 'tipo': 'ortografia'},
    'lecionario': {'sugestoes': ['lecionário'], 'tipo': 'ortografia'},
    'formulario': {'sugestoes': ['formulário'], 'tipo': 'ortografia'},
    'diario': {'sugestoes': ['diário'], 'tipo': 'ortografia'},
    'sacrario': {'sugestoes': ['sacrário'], 'tipo': 'ortografia'},
    'relatorio': {'sugestoes': ['relatório'], 'tipo': 'ortografia'},
    'territorio': {'sugestoes': ['território'], 'tipo': 'ortografia'},
    'dormitorio': {'sugestoes': ['dormitório'], 'tipo': 'ortografia'},
    'refeitorio': {'sugestoes': ['refeitório'], 'tipo': 'ortografia'},
    'audiotorio': {'sugestoes': ['auditório'], 'tipo': 'ortografia'},
    'conservatorio': {'sugestoes': ['conservatório'], 'tipo': 'ortografia'},
    'laboratorio': {'sugestoes': ['laboratório'], 'tipo': 'ortografia'},
    'senatorio': {'sugestoes': ['senado'], 'tipo': 'ortografia'},
    'seminario': {'sugestoes': ['seminário'], 'tipo': 'ortografia'},
    'sanatorio': {'sugestoes': ['sanatório'], 'tipo': 'ortografia'},
    'dispensario': {'sugestoes': ['dispensário'], 'tipo': 'ortografia'},
    'anuario': {'sugestoes': ['anuário'], 'tipo': 'ortografia'},
    'breviario': {'sugestoes': ['breviário'], 'tipo': 'ortografia'},
    'rosario': {'sugestoes': ['rosário'], 'tipo': 'ortografia'},
    'hipocrisia': {'sugestoes': ['hipocrisia'], 'tipo': 'ortografia'},
    'paralisia': {'sugestoes': ['paralisia'], 'tipo': 'ortografia'},
    'catalise': {'sugestoes': ['catálise'], 'tipo': 'ortografia'},
    'analise': {'sugestoes': ['análise'], 'tipo': 'ortografia'},
    'sintese': {'sugestoes': ['síntese'], 'tipo': 'ortografia'},
    'hipotese': {'sugestoes': ['hipótese'], 'tipo': 'ortografia'},
    'tese': {'sugestoes': ['tese'], 'tipo': 'ortografia'},
    'antitese': {'sugestoes': ['antítese'], 'tipo': 'ortografia'},
    'prognose': {'sugestoes': ['prognose'], 'tipo': 'ortografia'},
    'diagnostico': {'sugestoes': ['diagnóstico'], 'tipo': 'ortografia'},
    'sismos': {'sugestoes': ['sismos'], 'tipo': 'ortografia'},
    'plasma': {'sugestoes': ['plasma'], 'tipo': 'ortografia'},
    
    # Verbos comuns e conjugações (60+)
    'clica': {'sugestoes': ['clicar'], 'tipo': 'verbo'},
    'seleciona': {'sugestoes': ['selecionar'], 'tipo': 'verbo'},
    'inseri': {'sugestoes': ['inserir'], 'tipo': 'verbo'},
    'exibi': {'sugestoes': ['exibir'], 'tipo': 'verbo'},
    'preenchi': {'sugestoes': ['preencher'], 'tipo': 'verbo'},
    'verrificar': {'sugestoes': ['verificar'], 'tipo': 'verbo'},
    'verifica': {'sugestoes': ['verificar'], 'tipo': 'verbo'},
    'processa': {'sugestoes': ['processar'], 'tipo': 'verbo'},
    'procesi': {'sugestoes': ['processar'], 'tipo': 'verbo'},
    'conferir': {'sugestoes': ['conferir'], 'tipo': 'verbo'},
    'conferiu': {'sugestoes': ['conferiu'], 'tipo': 'verbo'},
    'conferir': {'sugestoes': ['conferir'], 'tipo': 'verbo'},
    'arumar': {'sugestoes': ['arrumar'], 'tipo': 'verbo'},
    'corrigir': {'sugestoes': ['corrigir'], 'tipo': 'verbo'},
    'edita': {'sugestoes': ['editar'], 'tipo': 'verbo'},
    'delete': {'sugestoes': ['deletar', 'apagar'], 'tipo': 'verbo'},
    'sava': {'sugestoes': ['salvar'], 'tipo': 'verbo'},
    'envia': {'sugestoes': ['enviar'], 'tipo': 'verbo'},
    'receba': {'sugestoes': ['receber'], 'tipo': 'verbo'},
    'aceptar': {'sugestoes': ['aceitar'], 'tipo': 'verbo'},
    'rejeita': {'sugestoes': ['rejeitar'], 'tipo': 'verbo'},
    'configura': {'sugestoes': ['configurar'], 'tipo': 'verbo'},
    'personaliza': {'sugestoes': ['personalizar'], 'tipo': 'verbo'},
    'ativa': {'sugestoes': ['ativar'], 'tipo': 'verbo'},
    'desativa': {'sugestoes': ['desativar'], 'tipo': 'verbo'},
    'vincula': {'sugestoes': ['vincular'], 'tipo': 'verbo'},
    'desvincula': {'sugestoes': ['desvincular'], 'tipo': 'verbo'},
    'sincroniza': {'sugestoes': ['sincronizar'], 'tipo': 'verbo'},
    'exporta': {'sugestoes': ['exportar'], 'tipo': 'verbo'},
    'importa': {'sugestoes': ['importar'], 'tipo': 'verbo'},
    'criptografa': {'sugestoes': ['criptografar'], 'tipo': 'verbo'},
    'descriptografa': {'sugestoes': ['descriptografar'], 'tipo': 'verbo'},
    'valida': {'sugestoes': ['validar'], 'tipo': 'verbo'},
    'invalida': {'sugestoes': ['invalidar'], 'tipo': 'verbo'},
    'autoriza': {'sugestoes': ['autorizar'], 'tipo': 'verbo'},
    'desautoriza': {'sugestoes': ['desautorizar'], 'tipo': 'verbo'},
    'delega': {'sugestoes': ['delegar'], 'tipo': 'verbo'},
    'escalona': {'sugestoes': ['escalonar'], 'tipo': 'verbo'},
    'prioriza': {'sugestoes': ['priorizar'], 'tipo': 'verbo'},
    'documenta': {'sugestoes': ['documentar'], 'tipo': 'verbo'},
    'registra': {'sugestoes': ['registrar'], 'tipo': 'verbo'},
    'arquiva': {'sugestoes': ['arquivar'], 'tipo': 'verbo'},
    'restaura': {'sugestoes': ['restaurar'], 'tipo': 'verbo'},
    'backup': {'sugestoes': ['fazer backup'], 'tipo': 'verbo'},
    'monitora': {'sugestoes': ['monitorar'], 'tipo': 'verbo'},
    'otimiza': {'sugestoes': ['otimizar'], 'tipo': 'verbo'},
    'fragmanta': {'sugestoes': ['fragmentar'], 'tipo': 'verbo'},
    'desfragmanta': {'sugestoes': ['desfragmentar'], 'tipo': 'verbo'},
    'compacta': {'sugestoes': ['compactar'], 'tipo': 'verbo'},
    'descompacta': {'sugestoes': ['descompactar'], 'tipo': 'verbo'},
    'encrypta': {'sugestoes': ['encriptar'], 'tipo': 'verbo'},
    'decrypta': {'sugestoes': ['decriptar'], 'tipo': 'verbo'},
    
    # Palavras com digitação duplicada (comum em teclado rápido)
    'palavrras': {'sugestoes': ['palavras'], 'tipo': 'ortografia'},
    'eradas': {'sugestoes': ['erradas'], 'tipo': 'ortografia'},
    'todass': {'sugestoes': ['todas'], 'tipo': 'ortografia'},
    'tesste': {'sugestoes': ['teste'], 'tipo': 'ortografia'},
    'textes': {'sugestoes': ['texto', 'textos'], 'tipo': 'ortografia'},
    'senhor': {'sugestoes': ['senhor'], 'tipo': 'ortografia'},
    'senhhor': {'sugestoes': ['senhor'], 'tipo': 'ortografia'},
    'ee': {'sugestoes': ['e'], 'tipo': 'digitacao'},
    'oo': {'sugestoes': ['o'], 'tipo': 'digitacao'},
    
    # Concordância e uso comum
    'o dados': {'sugestoes': ['os dados'], 'tipo': 'concordancia'},
    'o usuario': {'sugestoes': ['o usuário'], 'tipo': 'concordancia'},
    'a usuarios': {'sugestoes': ['aos usuários', 'as usuárias'], 'tipo': 'concordancia'},
    'di': {'sugestoes': ['de'], 'tipo': 'ortografia'},
}

# Padrões regex para detectar erros
PADROES = [
    # Palavras dobradas
    (r'\b(\w+)\s+\1\b', 'palavra_duplicada'),
    # Espaços múltiplos
    (r'  +', 'espacos_multiplos'),
    # Pontuação dupla
    (r'\.{2,}', 'pontuacao_dupla'),
    # Vírgulas mal colocadas
    (r' ,', 'virgula_mal_colocada'),
]


class CorretorGramatical:
    """Corretor gramatical leve para português brasileiro"""
    
    def __init__(self):
        """Inicializa o corretor"""
        self.disponivel = True
        self.erros_encontrados = 0
        print("[OK] Corretor gramatical PT-BR inicializado (versão leve)")
    
    def verificar_palavra(self, palavra: str) -> Optional[Dict]:
        """
        Verifica se uma palavra tem erro conhecido
        
        Args:
            palavra: Palavra a verificar
            
        Returns:
            Dicionário com informações do erro ou None
        """
        palavra_lower = palavra.lower()
        
        if palavra_lower in ERROS_COMUNS:
            erro_info = ERROS_COMUNS[palavra_lower].copy()
            erro_info['palavra'] = palavra
            return erro_info
        
        return None
    
    def verificar_texto(self, texto: str) -> List[Dict]:
        """
        Verifica erros gramaticais em um texto
        
        Args:
            texto: Texto a verificar
            
        Returns:
            Lista de erros encontrados
        """
        erros = []
        
        # Verificar palavras individuais
        palavras = re.findall(r'\b\w+\b', texto)
        posicao_atual = 0
        
        for palavra in palavras:
            pos = texto.find(palavra, posicao_atual)
            if pos >= 0:
                erro = self.verificar_palavra(palavra)
                if erro:
                    erros.append({
                        'posicao': (pos, pos + len(palavra)),
                        'texto_original': palavra,
                        'mensagem': f"Possível erro de {erro['tipo']}",
                        'sugestoes': erro['sugestoes'],
                        'tipo_erro': erro['tipo']
                    })
                posicao_atual = pos + len(palavra)
        
        # Verificar padrões
        for padrao, tipo_erro in PADROES:
            for match in re.finditer(padrao, texto):
                erros.append({
                    'posicao': match.span(),
                    'texto_original': match.group(),
                    'mensagem': f"Erro: {tipo_erro}",
                    'sugestoes': [],
                    'tipo_erro': tipo_erro
                })
        
        # Remover duplicatas baseadas em posição
        erros_unicos = []
        posicoes_vistas = set()
        for erro in sorted(erros, key=lambda x: x['posicao'][0]):
            if erro['posicao'] not in posicoes_vistas:
                erros_unicos.append(erro)
                posicoes_vistas.add(erro['posicao'])
        
        return erros_unicos
    
    def corrigir_texto(self, texto: str, automatico: bool = False) -> Tuple[str, List[Dict]]:
        """
        Corrige erros gramaticais em um texto
        
        Args:
            texto: Texto a corrigir
            automatico: Se True, aplica melhor sugestão automaticamente
            
        Returns:
            Tupla (texto_corrigido, lista_de_erros)
        """
        erros = self.verificar_texto(texto)
        
        if not erros:
            return texto, []
        
        # Ordenar por posição reversa para não quebrar índices
        erros_ordenados = sorted(erros, key=lambda x: x['posicao'][0], reverse=True)
        
        texto_corrigido = texto
        erros_aplicados = []
        
        for erro in erros_ordenados:
            inicio, fim = erro['posicao']
            texto_original = texto_corrigido[inicio:fim]
            
            if automatico and erro['sugestoes']:
                sugestao = erro['sugestoes'][0]
                texto_corrigido = (
                    texto_corrigido[:inicio] + 
                    sugestao + 
                    texto_corrigido[fim:]
                )
                erros_aplicados.append({
                    'original': texto_original,
                    'corrigido': sugestao,
                    'mensagem': erro['mensagem']
                })
            else:
                erros_aplicados.append({
                    'original': texto_original,
                    'sugestoes': erro['sugestoes'],
                    'mensagem': erro['mensagem']
                })
        
        return texto_corrigido, erros_aplicados
    
    def gerar_relatorio(self, texto: str) -> str:
        """
        Gera relatório formatado de erros
        
        Args:
            texto: Texto a analisar
            
        Returns:
            Relatório em formato texto
        """
        erros = self.verificar_texto(texto)
        
        if not erros:
            return "✅ Nenhum erro gramatical detectado!"
        
        relatorio = f"❌ {len(erros)} erro(s) encontrado(s):\n\n"
        
        for idx, erro in enumerate(erros, 1):
            relatorio += f"{idx}. '{erro['texto_original']}' (Posição {erro['posicao'][0]})\n"
            relatorio += f"   Problema: {erro['mensagem']}\n"
            
            if erro['sugestoes']:
                relatorio += f"   Sugestões: {', '.join(erro['sugestoes'])}\n"
            
            relatorio += f"   Tipo: {erro['tipo_erro']}\n\n"
        
        return relatorio


def corrigir_json_manual(dados_json: Dict, automatico: bool = False) -> Tuple[Dict, Dict]:
    """
    Corrige erros em JSON de manual
    
    Args:
        dados_json: Dicionário com dados do manual
        automatico: Se True, aplica correções
        
    Returns:
        Tupla (json_corrigido, relatorio)
    """
    corretor = CorretorGramatical()
    dados_corrigidos = dados_json.copy()
    relatorio = {'campos_corrigidos': []}
    
    # Corrigir objetivo
    if 'objetivo' in dados_json:
        objetivo_corrigido, erros = corretor.corrigir_texto(
            dados_json['objetivo'],
            automatico=automatico
        )
        if erros:
            dados_corrigidos['objetivo'] = objetivo_corrigido
            relatorio['campos_corrigidos'].append({
                'campo': 'objetivo',
                'erros': len(erros),
                'detalhes': erros
            })
    
    # Corrigir pré-requisito
    if 'pre_requisito' in dados_json:
        pre_corrigido, erros = corretor.corrigir_texto(
            dados_json['pre_requisito'],
            automatico=automatico
        )
        if erros:
            dados_corrigidos['pre_requisito'] = pre_corrigido
            relatorio['campos_corrigidos'].append({
                'campo': 'pre_requisito',
                'erros': len(erros),
                'detalhes': erros
            })
    
    # Corrigir funcionalidades
    if 'funcionalidades' in dados_json:
        funcionalidades_corrigidas = []
        
        for idx, func in enumerate(dados_json['funcionalidades']):
            func_corrigida = func.copy()
            mudancas_func = []
            
            # Corrigir título
            if 'titulo' in func:
                titulo_corrigido, erros = corretor.corrigir_texto(
                    func['titulo'],
                    automatico=automatico
                )
                if erros:
                    func_corrigida['titulo'] = titulo_corrigido
                    mudancas_func.append({'campo': 'titulo', 'erros': len(erros)})
            
            # Corrigir descrição
            if 'descricao' in func:
                desc_corrigida, erros = corretor.corrigir_texto(
                    func['descricao'],
                    automatico=automatico
                )
                if erros:
                    func_corrigida['descricao'] = desc_corrigida
                    mudancas_func.append({'campo': 'descricao', 'erros': len(erros)})
            
            # Corrigir observações
            if 'observacoes' in func and func['observacoes']:
                obs_corrigidas = []
                for obs in func['observacoes']:
                    obs_corrigida, erros = corretor.corrigir_texto(
                        obs,
                        automatico=automatico
                    )
                    obs_corrigidas.append(obs_corrigida)
                
                if obs_corrigidas != func['observacoes']:
                    func_corrigida['observacoes'] = obs_corrigidas
                    mudancas_func.append({'campo': 'observacoes', 'itens': len(obs_corrigidas)})
            
            if mudancas_func:
                relatorio['campos_corrigidos'].append({
                    'funcionalidade': f"{idx + 1} - {func.get('titulo', 'N/A')}",
                    'mudancas': mudancas_func
                })
            
            funcionalidades_corrigidas.append(func_corrigida)
        
        dados_corrigidos['funcionalidades'] = funcionalidades_corrigidas
    
    return dados_corrigidos, relatorio


def main():
    """Interface CLI"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python corretor_gramatical.py <arquivo.json> [--automatico]")
        print("\nExemplos:")
        print("  python corretor_gramatical.py manual_input.json")
        print("  python corretor_gramatical.py manual_input.json --automatico")
        sys.exit(1)
    
    arquivo_json = sys.argv[1]
    automatico = '--automatico' in sys.argv
    
    try:
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        print(f"[INFO] Corrigindo '{arquivo_json}'...")
        
        dados_corrigidos, relatorio = corrigir_json_manual(dados, automatico=automatico)
        
        if relatorio['campos_corrigidos']:
            print(f"\n✅ {len(relatorio['campos_corrigidos'])} campo(s) com erros:\n")
            for item in relatorio['campos_corrigidos']:
                print(f"  • {item.get('campo') or item.get('funcionalidade')}")
        else:
            print("\n✅ Nenhum erro gramatical detectado!")
        
        if dados_corrigidos != dados and automatico:
            arquivo_corrigido = arquivo_json.replace('.json', '_corrigido.json')
            with open(arquivo_corrigido, 'w', encoding='utf-8') as f:
                json.dump(dados_corrigidos, f, ensure_ascii=False, indent=2)
            print(f"\n[OK] Arquivo corrigido salvo: {arquivo_corrigido}")
    
    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {arquivo_json}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"[ERRO] JSON inválido em {arquivo_json}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERRO] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

