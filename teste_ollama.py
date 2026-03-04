#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste: Ollama API Local
Verifica se o servidor Ollama está rodando e testando models
"""

import requests
import json
import sys
from typing import Optional

# Configuração
OLLAMA_URL = "http://localhost:11434"
MODELS = ["neural-chat", "mistral", "llama2", "orca-mini"]

def test_connection() -> bool:
    """Testa conexão com Ollama"""
    print("🔍 Testando conexão com Ollama...")
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Conexão OK! Ollama está rodando em http://localhost:11434")
            return True
        else:
            print(f"❌ Erro de conexão: Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não consegui conectar ao Ollama em http://localhost:11434")
        print("   Certifique-se de que:")
        print("   1. Ollama está instalado (https://ollama.ai)")
        print("   2. Execute: ollama serve")
        print("   3. Deixe o terminal aberto enquanto usa a aplicação")
        return False
    except requests.exceptions.Timeout:
        print("❌ Conexão timeout. Verifique se Ollama está respondendo.")
        return False

def list_models() -> list:
    """Lista modelos disponíveis"""
    print("\n📚 Modelos disponíveis:")
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        data = response.json()
        models = data.get('models', [])
        
        if models:
            for model in models:
                size_gb = model['size'] / (1024**3)
                print(f"  • {model['name']:<20} ({size_gb:.2f} GB)")
            return [m['name'] for m in models]
        else:
            print("  ❌ Nenhum modelo encontrado")
            print("  Execute: ollama pull neural-chat")
            return []
    except Exception as e:
        print(f"  ❌ Erro ao listar modelos: {e}")
        return []

def test_model(model_name: str) -> Optional[str]:
    """Testa correção de texto com modelo específico"""
    test_text = "tesste de ortografia senario de textes"
    prompt = f"Corrija o texto português mantendo apenas o resultado: '{test_text}'"
    
    print(f"\n🧪 Testando modelo: {model_name}")
    print(f"   Texto: {test_text}")
    
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            corrected = result.get('response', '').strip()
            print(f"   ✅ Resultado: {corrected[:80]}...")
            return corrected
        else:
            print(f"   ❌ Erro: Status {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print(f"   ⏱️ Timeout - Modelo pode estar processando lentamente")
        return None
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Perdeu conexão com Ollama")
        return None
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None

def find_available_model() -> Optional[str]:
    """Encontra primeiro modelo disponível"""
    models = list_models()
    if models:
        return models[0]
    return None

def main():
    print("=" * 70)
    print("TESTE: Ollama API Local para Correção Ortográfica")
    print("=" * 70)
    
    # 1. Testar conexão
    if not test_connection():
        print("\n❌ Não foi possível conectar ao Ollama")
        print("\n📋 Para resolver:")
        print("   1. Instale Ollama: https://ollama.ai/download/windows")
        print("   2. Abra PowerShell como Administrador")
        print("   3. Execute: ollama serve")
        print("   4. Mantenha o terminal aberto")
        return 1
    
    # 2. Listar modelos
    models = list_models()
    
    if not models:
        print("\n❌ Nenhum modelo instalado")
        print("\n📋 Para resolver:")
        print("   1. Abra novo PowerShell")
        print("   2. Execute: ollama pull neural-chat")
        print("   3. Aguarde o download (~6-7GB)")
        print("   4. Depois rode este script novamente")
        return 1
    
    # 3. Testar primeiro modelo disponível
    print("\n" + "-" * 70)
    model_to_test = models[0]
    result = test_model(model_to_test)
    
    if result:
        print("\n" + "=" * 70)
        print("✅ TUDO OK! Ollama está pronto para usar")
        print(f"   Modelo: {model_to_test}")
        print(f"   URL: http://localhost:11434")
        print("=" * 70)
        return 0
    else:
        print("\n❌ Erro ao testar modelo")
        return 1

if __name__ == "__main__":
    sys.exit(main())
