#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste isolado da verificação gramatical na interface
"""

from src.corretor_gramatical import corrigir_json_manual

# Simular dados do formulário
dados = {
    "objetivo": "tesste di otografia senario de textes inclusao calcao verrificar palavrras eradas e arumar todass",
    "pre_requisito": "usuario modulo funcao",
    "funcionalidades": [
        {
            "titulo": "Criar Item",
            "descricao": "proceso do usuario",
            "observacoes": []
        }
    ]
}

print("=" * 70)
print("TESTE: Verificação Gramatical (Modo Manual)")
print("=" * 70)

print("\n📝 Dados inseridos:")
print(f"Objetivo: {dados['objetivo']}")
print(f"Pré-requisito: {dados['pre_requisito']}")
print(f"Descrição: {dados['funcionalidades'][0]['descricao']}")

print("\n🔍 Executando verificação SEM autocorreção...")
dados_corrigidos, relatorio = corrigir_json_manual(dados, automatico=False)

print("\n📊 Resultado:")
print(f"Campos com erros: {len(relatorio['campos_corrigidos'])}")

if relatorio['campos_corrigidos']:
    print("\n❌ Erros encontrados:")
    for item in relatorio['campos_corrigidos']:
        print(f"\n  Campo: {item.get('campo', item.get('funcionalidade', 'desconhecido'))}")
        print(f"  Texto: {item['texto_original'][:60]}...")
        print(f"  Erros: {len(item['erros'])}")
        for erro in item['erros'][:3]:
            print(f"    - '{erro['texto_original']}' → {erro['sugestoes']}")
else:
    print("\n✅ Nenhum erro encontrado!")

print("\n" + "=" * 70)
print("Agora testando com AUTOCORREÇÃO ativa...")
print("=" * 70)

dados_corrigidos, relatorio = corrigir_json_manual(dados, automatico=True)

print("\n✅ Dados corrigidos:")
print(f"Objetivo: {dados_corrigidos['objetivo']}")
print(f"Pré-requisito: {dados_corrigidos['pre_requisito']}")
print(f"Descrição: {dados_corrigidos['funcionalidades'][0]['descricao']}")

print("\n📊 Totalizador:")
print(f"Total de correções: {sum(len(item['erros']) for item in relatorio['campos_corrigidos'])}")
