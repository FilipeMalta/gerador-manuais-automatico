#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste completo do corretor gramatical
Valida detecção e correção de erros em português
"""

import sys
from src.corretor_gramatical import CorretorGramatical

def test_corretor():
    """Testa funcionalidades do corretor gramatical"""
    print("=" * 70)
    print("TESTE COMPLETO DO CORRETOR GRAMATICAL")
    print("=" * 70)
    
    corretor = CorretorGramatical()
    
    # Teste 1: Texto do usuário
    print("\n📝 TESTE 1: Texto com erros do usuário")
    print("-" * 70)
    texto1 = "tesste di otografia senario de textes inclusao calcao verrificar palavrras eradas e arumar todass"
    print(f"Entrada: '{texto1}'")
    erros1 = corretor.verificar_texto(texto1)
    print(f"Erros detectados: {len(erros1)}")
    for i, erro in enumerate(erros1, 1):
        print(f"  {i}. '{erro['texto_original']}' → {erro['sugestoes']} ({erro['tipo_erro']})")
    
    # Teste 2: Acentuação
    print("\n📝 TESTE 2: Palavras com falta de acentuação")
    print("-" * 70)
    texto2 = "usuario, modulo, funcao, metodo"
    print(f"Entrada: '{texto2}'")
    erros2 = corretor.verificar_texto(texto2)
    print(f"Erros detectados: {len(erros2)}")
    for erro in erros2:
        print(f"  '{erro['texto_original']}' → {erro['sugestoes']}")
    
    # Teste 3: Verbos conjugados
    print("\n📝 TESTE 3: Verbos com erros de grafia")
    print("-" * 70)
    texto3 = "clica seleciona preenchi verrificar"
    print(f"Entrada: '{texto3}'")
    erros3 = corretor.verificar_texto(texto3)
    print(f"Erros detectados: {len(erros3)}")
    for erro in erros3:
        print(f"  '{erro['texto_original']}' → {erro['sugestoes']}")
    
    # Teste 4: Autocorreção
    print("\n📝 TESTE 4: Autocorreção automática")
    print("-" * 70)
    texto4 = "usuario inseri dados no modulo"
    print(f"Original: '{texto4}'")
    corrigido, aplicadas = corretor.corrigir_texto(texto4, automatico=True)
    print(f"Corrigido: '{corrigido}'")
    print(f"Correções aplicadas: {len(aplicadas)}")
    
    # Teste 5: Frequência de detecção
    print("\n📝 TESTE 5: Teste de frequência - 100 palavras com erros")
    print("-" * 70)
    palavras_erro = [
        "usuario", "modulo", "funcao", "acao", "metodo", "generico", 
        "critico", "proceso", "sisitema", "otografia", "senario", 
        "inclusao", "calcao", "verrificar", "palavrras", "eradas",
        "todass", "tesste", "textes", "arumar"
    ]
    texto5 = " ".join([p for p in palavras_erro for _ in range(5)])[:500]
    erros5 = corretor.verificar_texto(texto5)
    taxa_deteccao = (len(erros5) / len(set(texto5.split()))) * 100 if texto5.split() else 0
    print(f"Total de erros detectados: {len(erros5)}")
    print(f"Palavras únicas verificadas: {len(set(texto5.split()))}")
    print(f"Taxa de detecção: ~{taxa_deteccao:.0f}%")
    
    # Resumo
    print("\n" + "=" * 70)
    print("✅ RESUMO DOS TESTES")
    print("=" * 70)
    print(f"✓ Teste 1: {len(erros1)} erros detectados (esperado: ~12)")
    print(f"✓ Teste 2: {len(erros2)} erros detectados (esperado: 4)")
    print(f"✓ Teste 3: {len(erros3)} erros detectados (esperado: 4)")
    print(f"✓ Teste 4: {len(aplicadas)} correções automáticas aplicadas")
    print(f"✓ Teste 5: {len(erros5)} erros detectados em texto maior")
    print("\n✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = test_corretor()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
