#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testes para o Corretor Gramatical PT-BR
Versão 2.0 - Teste da versão leve (sem dependências pesadas)
"""

import sys
import json
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from corretor_gramatical import CorretorGramatical, corrigir_json_manual


def test_verificacao():
    """Teste 1: Verificar erros em texto"""
    print("=" * 60)
    print("Teste 1: Verificação de Erros")
    print("=" * 60)
    
    corretor = CorretorGramatical()
    
    textos_teste = [
        "O usuario  clicou no botao",  # espaços múltiplos
        "sistema modulo funcao",  # acentuação
        "inseri o dados no proceso",  # verbo e ortografia
        "Nenhum erro neste texto correto!",  # sem erros
        "palavra palavra repetida",  # palavra duplicada
    ]
    
    for idx, texto in enumerate(textos_teste, 1):
        print(f"\n{idx}. Texto: '{texto}'")
        erros = corretor.verificar_texto(texto)
        
        if erros:
            print(f"   ❌ {len(erros)} erro(s) encontrado(s):")
            for erro in erros:
                print(f"      - '{erro['texto_original']}' → {erro['sugestoes'] if erro['sugestoes'] else '[sem sugestão]'}")
        else:
            print("   ✅ Nenhum erro encontrado!")


def test_correcao():
    """Teste 2: Corrigir erros com sugestões"""
    print("\n" + "=" * 60)
    print("Teste 2: Correção de Texto")
    print("=" * 60)
    
    corretor = CorretorGramatical()
    
    texto = "O usuario clicou no botao para verifica o dado"
    print(f"\nTexto original: '{texto}'")
    
    # Só com sugestões
    texto_sugerido, erros_sugeridos = corretor.corrigir_texto(texto, automatico=False)
    print(f"\nRelatório de erros (sem auto-correção):")
    if erros_sugeridos:
        for erro in erros_sugeridos:
            print(f"  • '{erro['original']}' → {erro.get('sugestoes', [])}")
    else:
        print("  ✅ Nenhum erro para corrigir")
    
    # Com auto-correção
    print(f"\nAuto-corrigindo...")
    texto_corrigido, erros_corrigidos = corretor.corrigir_texto(texto, automatico=True)
    print(f"Texto corrigido: '{texto_corrigido}'")
    print(f"Correções aplicadas: {len(erros_corrigidos)}")


def test_relatorio():
    """Teste 3: Gerar relatório detalhado"""
    print("\n" + "=" * 60)
    print("Teste 3: Relatório Detalhado")
    print("=" * 60)
    
    corretor = CorretorGramatical()
    
    texto = """O usuario do sistema modulo deve seguir o processo correto.
    Inseri os dados no formulário e verificar o resultado.
    A acao foi concluida com sucesso."""
    
    print(f"\nTexto a analisar:")
    print(f"{texto}\n")
    
    relatorio = corretor.gerar_relatorio(texto)
    print(relatorio)


def test_json():
    """Teste 4: Corrigir JSON de manual"""
    print("\n" + "=" * 60)
    print("Teste 4: Correção de JSON de Manual")
    print("=" * 60)
    
    dados_json = {
        "nome_manual": "Manual de Usuario",  # acentuação
        "objetivo": "Ensina o usuario a usar o sistema modulo de forma correta.",
        "pre_requisito": "O usuario deve ter acesso ao sistema",
        "funcionalidades": [
            {
                "titulo": "Logar no Sistema",
                "descricao": "Clica na tela de login e inseri sus dados",  # verbo e acentuação
                "observacoes": [
                    "A senha deve ser correta",
                    "O usuario nao  pode errar  multiplas vezes"  # espaços
                ]
            },
            {
                "titulo": "Crear Nova Funcao",  # acentuação
                "descricao": "Seleciona novo modulo e configura parametros",
                "observacoes": []
            }
        ]
    }
    
    print("\n📋 Analisando JSON...")
    dados_corrigidos, relatorio = corrigir_json_manual(dados_json, automatico=False)
    
    print(f"\n✅ Análise Completa!")
    print(f"Campos verificados: {len(relatorio.get('campos_corrigidos', []))}")
    
    if relatorio['campos_corrigidos']:
        print(f"\nCampos com erros:")
        for item in relatorio['campos_corrigidos']:
            campo = item.get('campo') or item.get('funcionalidade')
            mudancas = len(item.get('mudancas', [])) if 'mudancas' in item else item.get('erros', 0)
            print(f"  • {campo}: {mudancas} problema(s)")
    
    # Teste auto-correção
    print("\n\n🔧 Aplicando auto-correção...")
    dados_auto_corrigidos, relatorio_auto = corrigir_json_manual(dados_json, automatico=True)
    print(f"✅ Auto-correção aplicada!")
    
    # Mostrar diferenças
    if dados_auto_corrigidos != dados_json:
        print("\n📝 Exemplo de correção:")
        if 'objetivo' in dados_json:
            if dados_auto_corrigidos.get('objetivo') != dados_json.get('objetivo'):
                print(f"  Original: {dados_json['objetivo'][:50]}...")
                print(f"  Corrigido: {dados_auto_corrigidos['objetivo'][:50]}...")


if __name__ == "__main__":
    try:
        test_verificacao()
        test_correcao()
        test_relatorio()
        test_json()
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n❌ ERRO NOS TESTES: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
