#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integração Ollama com Sistema de Correção de Texto
Usa LLM local para correção ortográfica e gramatical em português
"""

import requests
import json
from typing import Optional, Dict, Tuple
import time

class CorretorOllama:
    """Corretor de texto usando Ollama local"""
    
    def __init__(self, 
                 url: str = "http://localhost:11434",
                 model: str = "neural-chat",
                 timeout: int = 60):
        """
        Inicializar corretor Ollama
        
        Args:
            url: URL do servidor Ollama
            model: Nome do modelo (neural-chat, mistral, llama2, etc)
            timeout: Timeout em segundos para requisições
        """
        self.url = url
        self.model = model
        self.timeout = timeout
        self.disponivel = False
        
    def verificar_disponibilidade(self) -> bool:
        """Verifica se Ollama está disponível e modelo está carregado"""
        try:
            response = requests.get(f"{self.url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                self.disponivel = self.model in model_names
                return self.disponivel
        except Exception:
            self.disponivel = False
            return False
    
    def corrigir_texto(self, texto: str) -> Tuple[str, bool]:
        """
        Corrige texto usando LLM local
        
        Args:
            texto: Texto a corrigir
            
        Returns:
            Tupla (texto_corrigido, sucesso)
        """
        if not self.disponivel:
            return texto, False
        
        if not texto or len(texto.strip()) == 0:
            return texto, False
        
        # Prompt otimizado para correção
        prompt = f"""Você é um corretor ortográfico profissional de português brasileiro.
Corrija o texto abaixo mantendo o significado e o tom original.
Retorne APENAS o texto corrigido, sem explicações.

Texto: {texto}

Texto corrigido:"""
        
        try:
            response = requests.post(
                f"{self.url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.1  # Temperatura baixa para consistência
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                texto_corrigido = result.get('response', '').strip()
                
                # Limpar output do modelo (às vezes adiciona prefixos)
                if texto_corrigido.startswith('Texto corrigido:'):
                    texto_corrigido = texto_corrigido[len('Texto corrigido:'):].strip()
                
                return texto_corrigido, True
            else:
                return texto, False
                
        except requests.exceptions.Timeout:
            return texto, False
        except requests.exceptions.ConnectionError:
            return texto, False
        except Exception:
            return texto, False
    
    def corrigir_json_manual(self, dados: Dict, campos: list = None) -> Tuple[Dict, Dict]:
        """
        Corrige campos de um JSON de manual
        
        Args:
            dados: Dicionário com dados do manual
            campos: Lista de campos a corrigir ['objetivo', 'pre_requisito', 'descricao']
            
        Returns:
            Tupla (dados_corrigidos, relatorio)
        """
        if campos is None:
            campos = ['objetivo', 'pre_requisito']
        
        dados_corrigidos = dados.copy()
        relatorio = {'campos_corrigidos': [], 'erros': []}
        
        if not self.disponivel:
            relatorio['erros'].append('Ollama não está disponível')
            return dados, relatorio
        
        # Corrigir objetivo
        if 'objetivo' in campos and 'objetivo' in dados:
            original = dados['objetivo']
            corrigido, sucesso = self.corrigir_texto(original)
            
            if sucesso and corrigido != original:
                dados_corrigidos['objetivo'] = corrigido
                relatorio['campos_corrigidos'].append({
                    'campo': 'objetivo',
                    'original': original[:50] + '...',
                    'corrigido': corrigido[:50] + '...'
                })
        
        # Corrigir pré-requisito
        if 'pre_requisito' in campos and 'pre_requisito' in dados:
            original = dados['pre_requisito']
            corrigido, sucesso = self.corrigir_texto(original)
            
            if sucesso and corrigido != original:
                dados_corrigidos['pre_requisito'] = corrigido
                relatorio['campos_corrigidos'].append({
                    'campo': 'pre_requisito',
                    'original': original[:50] + '...',
                    'corrigido': corrigido[:50] + '...'
                })
        
        # Corrigir funcionalidades
        if 'funcionalidades' in dados and 'descricao' in campos:
            funcionalidades_corrigidas = []
            
            for idx, func in enumerate(dados['funcionalidades']):
                func_corrigida = func.copy()
                
                if 'descricao' in func:
                    original = func['descricao']
                    corrigido, sucesso = self.corrigir_texto(original)
                    
                    if sucesso and corrigido != original:
                        func_corrigida['descricao'] = corrigido
                        relatorio['campos_corrigidos'].append({
                            'funcionalidade': func.get('titulo', f'Funcionalidade {idx+1}'),
                            'original': original[:50] + '...',
                            'corrigido': corrigido[:50] + '...'
                        })
                
                funcionalidades_corrigidas.append(func_corrigida)
            
            dados_corrigidos['funcionalidades'] = funcionalidades_corrigidas
        
        return dados_corrigidos, relatorio


def main():
    """Teste de integração"""
    print("=" * 70)
    print("Teste: Integração Ollama")
    print("=" * 70)
    
    # Criar corretor
    print("\n1️⃣ Inicializando corretor...")
    corretor = CorretorOllama()
    
    # Verificar disponibilidade
    print("2️⃣ Verificando disponibilidade do Ollama...")
    if corretor.verificar_disponibilidade():
        print(f"   ✅ Ollama disponível (modelo: {corretor.model})")
    else:
        print("   ❌ Ollama não está disponível")
        print("   Execute em outro terminal: ollama serve")
        return 1
    
    # Testar correção
    print("\n3️⃣ Testando correção de texto...")
    textos_teste = [
        "tesste de ortografia",
        "processo de criacao",
        "usuario deve clicar no modulo"
    ]
    
    for texto in textos_teste:
        corrigido, sucesso = corretor.corrigir_texto(texto)
        status = "✅" if sucesso else "❌"
        print(f"   {status} '{texto}'")
        if sucesso:
            print(f"      → '{corrigido}'")
    
    # Testar JSON
    print("\n4️⃣ Testando correção de JSON...")
    dados_teste = {
        "objetivo": "descrever o processo de criacao de items",
        "pre_requisito": "usuario com perfil de editor",
        "funcionalidades": [
            {
                "titulo": "Criar Item",
                "descricao": "processo para criar um novo item no sistema"
            }
        ]
    }
    
    dados_corrigidos, relatorio = corretor.corrigir_json_manual(dados_teste)
    print(f"   {len(relatorio['campos_corrigidos'])} campo(s) corrigido(s)")
    
    for item in relatorio['campos_corrigidos']:
        print(f"   • {item.get('campo', item.get('funcionalidade'))}")
    
    print("\n" + "=" * 70)
    print("✅ Integração OK! Ollama está pronto para usar")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
