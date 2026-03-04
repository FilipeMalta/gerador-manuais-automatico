# � Corretor Gramatical PT-BR v2.0

## Visão Geral

O **Corretor Gramatical** é um módulo integrado ao Gerador de Manuais que verifica e corrige erros gramaticais e ortográficos em português brasileiro, **sem dependências externas pesadas**.

**Versão**: 2.0.0  
**Tipo**: Baseado em padrões regex + dicionário  
**Dependências**: ✅ Zero (nenhuma!)  
**Status**: ✅ Ativo e Otimizado  

---

## ✨ Características

- ✅ **Zero Dependências**: Não precisa de Java, LanguageTool ou bibliotecas pesadas
- ✅ **Muito Rápido**: Baseado em padrões regex (5-20ms por texto)
- ✅ **PT-BR Otimizado**: Detecta erros comuns em português brasileiro
- ✅ **Integrado**: Funciona no Streamlit, CLI e como biblioteca Python
- ✅ **Seguro**: Graceful degradation - nunca quebra o processo
- ✅ **Leve**: Apenas ~300 linhas de código Python puro

---

## 🎯 Erros Detectados

### 1. Acentuação (50 palavras)
```
usuario → usuário
modulo → módulo
funcao → função
acao → ação
```

### 2. Ortografia (40 palavras)
```
proceso → processo
sisitema → sistema
seleçao → seleção
verificaçao → verificação
```

### 3. Verbos (30 palavras)
```
clica → clicar
seleciona → selecionar
inseri → inserir
exibi → exibir
```

### 4. Concordância (15 padrões)
```
o dados → os dados
o usuario → o usuário
```

### 5. Padrões Automáticos (10 regras)
```
palavra palavra → [palavra duplicada]
texto  com  espaços → [espaços múltiplos]
texto... → [pontuação dupla]
texto , → [vírgula mal colocada]
```

---

## 🚀 Como Usar

### 1️⃣ Via Streamlit (UI Web)

**Ao gerar um manual:**

1. Preencha todos os dados
2. Clique em **"✅ Verificar Erros"**
3. Veja o relatório com sugestões
4. (Opcional) Clique **"🔧 Auto-Corrigir"**
5. Gere o manual final

### 2️⃣ Via CLI (Linha de Comando)

#### Verificar erros:
```bash
python src/corretor_gramatical.py exemplos/input/manual_input.json
```

**Saída:**
```
[OK] Corretor gramatical PT-BR inicializado (versão leve)
[INFO] Corrigindo 'exemplos/input/manual_input.json'...

✅ 4 campo(s) com erros:

  • objetivo
  • pre_requisito
  • 1 - Logar no Sistema
  • 2 - Criar Nova Função
```

#### Auto-corrigir e salvar:
```bash
python src/corretor_gramatical.py exemplos/input/manual_input.json --automatico
```

**Saída:**
```
✅ Arquivo corrigido salvo: exemplos/input/manual_input_corrigido.json
```

### 3️⃣ Via Python (Programaticamente)

#### Verificar texto:
```python
from src.corretor_gramatical import CorretorGramatical

corretor = CorretorGramatical()

texto = "O usuario clicou no botao"
erros = corretor.verificar_texto(texto)

for erro in erros:
    print(f"'{erro['texto_original']}' → {erro['sugestoes']}")
```

#### Corrigir texto:
```python
texto = "O usuario clicou no botao"

# Com sugestões
texto_corrigido, erros = corretor.corrigir_texto(texto, automatico=False)

# Auto-correção
texto_corrigido, erros = corretor.corrigir_texto(texto, automatico=True)
print(texto_corrigido)  # "O usuário clicou no botão"
```

#### Gerar relatório:
```python
texto = "O usuario do sistema modulo deve seguir o processo."
relatorio = corretor.gerar_relatorio(texto)
print(relatorio)
```

#### Corrigir JSON de manual:
```python
from src.corretor_gramatical import corrigir_json_manual
import json

with open('manual_input.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Verificar
dados_corrigidos, relatorio = corrigir_json_manual(dados, automatico=False)

# Auto-corrigir
dados_corrigidos, relatorio = corrigir_json_manual(dados, automatico=True)

# Salvar
with open('manual_corrigido.json', 'w', encoding='utf-8') as f:
    json.dump(dados_corrigidos, f, ensure_ascii=False, indent=2)
```

---

## 📊 Estrutura de Dados

### Saída de `verificar_texto()`:
```python
[
    {
        'posicao': (2, 9),
        'texto_original': 'usuario',
        'mensagem': 'Possível erro de acentuacao',
        'sugestoes': ['usuário'],
        'tipo_erro': 'acentuacao'
    },
    ...
]
```

### Saída de `corrigir_json_manual()`:
```python
(
    {  # JSON corrigido
        'objetivo': 'Ensina o usuário...',
        'funcionalidades': [...]
    },
    {  # Relatório
        'campos_corrigidos': [
            {
                'campo': 'objetivo',
                'erros': 2,
                'detalhes': [...]
            }
        ]
    }
)
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Analisar Manual Completo
```python
import json
from src.corretor_gramatical import corrigir_json_manual

with open('manual_input.json', 'r', encoding='utf-8') as f:
    manual = json.load(f)

manual_corrigido, relatorio = corrigir_json_manual(manual)

print(f"Campos com problemas: {len(relatorio['campos_corrigidos'])}")
for item in relatorio['campos_corrigidos']:
    print(f"  • {item['campo']}")
```

### Exemplo 2: Processar Lote
```python
from pathlib import Path
from src.corretor_gramatical import corrigir_json_manual
import json

pasta_manuais = Path('manuais/')

for arquivo_json in pasta_manuais.glob('*.json'):
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    dados_corrigidos, _ = corrigir_json_manual(dados, automatico=True)
    
    with open(arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(dados_corrigidos, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {arquivo_json.name} corrigido")
```

### Exemplo 3: Gerar Relatório Detalhado
```python
from src.corretor_gramatical import CorretorGramatical

corretor = CorretorGramatical()

texto = """
O usuario do sistema modulo deve seguir o processo correto.
Inseri os dados no formulário e verificar o resultado.
A acao foi concluida com sucesso.
"""

relatorio = corretor.gerar_relatorio(texto)
print(relatorio)
```

---

## 📁 Campos Analisados

### ✅ Automaticamente Analisados
- `objetivo` (Descrição do módulo)
- `pre_requisito` (Requisitos necessários)
- `funcionalidades[].titulo` (Nome da funcionalidade)
- `funcionalidades[].descricao` (Descrição procedural)
- `funcionalidades[].observacoes[]` (Listas de observações)

### ❌ Não Analisados
- `metadata` (Dados estruturados e datas)
- `funcionalidades[].prints` (Caminhos de arquivo)
- `funcionalidades[].icones` (Nomes de ícones)

---

## ⚙️ Performance

| Operação | Tempo |
|----------|-------|
| Verificar 500 chars | ~5ms |
| Corrigir 500 chars | ~8ms |
| Verificar JSON típico | ~15ms |
| Corrigir JSON típico | ~20ms |
| Gerar relatório 1000 chars | ~10ms |

---

## 🔧 Estendendo o Corretor

### Adicionar Novo Erro:
```python
# Em src/corretor_gramatical.py
ERROS_COMUNS = {
    'sua_palavra': {
        'sugestoes': ['sugestao1', 'sugestao2'],
        'tipo': 'sua_categoria'
    },
    # ... outros
}
```

### Adicionar Novo Padrão Regex:
```python
PADROES = [
    (r'seu_regex_pattern', 'seu_tipo_erro'),
    # ... outros
]
```

---

## ⚠️ Limitações

### O que NÃO detecta:
- ❌ Erros contextuais (uso incorreto mas gramaticalmente correto)
- ❌ Semântica complex
- ❌ Análise profunda de pontuação
- ❌ Coesão textual

### O que DETECTA BEM:
- ✅ Acentuação
- ✅ Ortografia básica
- ✅ Verbos comuns
- ✅ Espaçamento
- ✅ Padrões simples

---

## 🎨 Integração Streamlit

No aplicativo web, você verá:

```
┌─────────────────────────────────┐
│ 🔍 Verificação Gramatical       │
│                                 │
│ [✅ Verificar Erros]            │
│ [🔧 Auto-Corrigir]             │
│                                 │
│ Campos com erros:               │
│ • objetivo: 2 erros             │
│ • descricao: 1 erro             │
└─────────────────────────────────┘
```

---

## 🧪 Testes

Execute os testes:
```bash
python teste_corretor_v2.py
```

Saída esperada:
```
[OK] Corretor gramatical PT-BR inicializado
============================================================
Teste 1: Verificação de Erros
============================================================
...
✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO
```

---

## 📈 Casos de Uso

1. **Verificação Pré-Geração**: Checar erros antes de gerar PDF
2. **Auto-Correção**: Corrigir automaticamente antes de publicar
3. **Auditoria**: Gerar relatório de qualidade de texto
4. **Lote**: Processar múltiplos manuais de uma vez
5. **CI/CD**: Integrar em pipeline de validação

---

## 🚀 Próximas Melhorias

- [ ] Dicionário customizável por usuário
- [ ] Diferentes níveis de severidade
- [ ] Suporte para múltiplos idiomas
- [ ] ML para contexto (futuro)
- [ ] Integração com Git hooks

---

## 📞 FAQ

**P: Preciso de Java instalado?**  
R: Não! Versão 2.0 não precisa de nenhuma dependência externa.

**P: Por que alguns erros não são detectados?**  
R: O dicionário contém ~150 palavras. Você pode estender adicionando em `ERROS_COMUNS`.

**P: A auto-correção é 100% confiável?**  
R: Não. Recomenda-se revisar sugestões para textos muito técnicos.

**P: Funciona offline?**  
R: Sim! Não depende de servidores externos.

---

## 📝 Changelog

### v2.0 (Atual - 2026)
- ✅ Versão leve sem dependências
- ✅ Baseada em regex + dicionário
- ✅ Integração Streamlit
- ✅ Suporte CLI completo
- ✅ ~150 palavras no dicionário

### v1.0 (Descontinuado)
- ❌ Usava LanguageTool (requer Java)

---

**Status**: ✅ Pronto para Uso  
**Linguagem**: Português Brasileiro  
**Licença**: MIT
