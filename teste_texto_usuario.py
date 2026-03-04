#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste rápido do corretor gramatical com o texto do usuário
"""

import sys
from src.corretor_gramatical import CorretorGramatical

# Texto testado pelo usuário
texto_usuario = "tesste di otografia senario de textes inclusao calcao verrificar palavrras eradas e arumar todass"

print("=" * 60)
print("TESTE DO CORRETOR GRAMATICAL")
print("=" * 60)
print(f"\n📝 Texto original:")
print(f"'{texto_usuario}'\n")

corretor = CorretorGramatical()

print("🔍 Verificando erros...")
erros = corretor.verificar_texto(texto_usuario)

if erros:
    print(f"\n✅ {len(erros)} erro(s) detectado(s):\n")
    for idx, erro in enumerate(erros, 1):
        print(f"{idx}. '{erro['texto_original']}'")
        print(f"   Sugestões: {erro['sugestoes']}")
        print(f"   Tipo: {erro['tipo_erro']}\n")
else:
    print("\n✅ Nenhum erro detectado!")

print("\n🔧 Auto-corrigindo...")
texto_corrigido, _ = corretor.corrigir_texto(texto_usuario, automatico=True)

print(f"✅ Corrigido:")
print(f"'{texto_corrigido}'")
print("\n" + "=" * 60)
