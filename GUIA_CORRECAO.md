# 🔍 Como Funciona a Correção Gramatical

## 📍 Quando a Correção é Aplicada?

**DURANTE A ESCRITA** - Antes de gerar o documento Word!

### Fluxo de Uso:

```
1. Preencher Dados
   ├─ Metadados (aba 1)
   ├─ Objetivo + Pré-requisitos (aba 2)
   └─ Funcionalidades (aba 3)
         ↓
2. Ir para Aba "Gerar Manual"
         ↓
3. ✅ NOVO! Clicar em "Verificar Erros" ou "Auto-Corrigir"
   ├─ Ver problemas encontrados
   └─ Aplicar correções (se desejar)
         ↓
4. 🚀 Clicar em "Gerar Manual .docx"
   └─ Documento gerado com texto corrigido
```

---

## 🎯 Botões na Aba "Gerar Manual"

### Botão 1: ✅ Verificar Erros

**O que faz:**
- 🔍 Analisa Objetivo, Pré-requisitos e Funcionalidades
- 📋 Lista todos os erros encontrados
- 💡 Mostra sugestões de correção

**Exemplo:**
```
⚠️ 3 campo(s) com erros:
  • objetivo
  • pre_requisito  
  • 1 - Logar no Sistema
```

**Quando usar:**
- Antes de gerar o manual
- Para auditar qualidade do texto
- Para revisar sugestões manualmente

---

### Botão 2: 🔧 Auto-Corrigir

**O que faz:**
- 🤖 Corrige automaticamente os erros
- ✅ Aplica a melhor sugestão em cada caso
- 📝 Mostra quantos campos foram corrigidos

**Exemplo:**
```
✅ 3 campo(s) corrigido(s)!

usuario → usuário
modulo → módulo
proceso → processo
```

**Quando usar:**
- Ao detectar muitos erros
- Para correção rápida
- Antes de finalizar o manual

---

## 🔄 Workflow Completo

### Opção A: Revisar Manualmente
```
1. Preencher dados
2. Clicar "✅ Verificar Erros"
3. Ver sugestões
4. Editar manualmente os campos
5. Clicar "🚀 Gerar Manual"
```

### Opção B: Corrigir Automaticamente
```
1. Preencher dados
2. Clicar "🔧 Auto-Corrigir"
3. Sistema corrige automaticamente
4. Revisar (opcional)
5. Clicar "🚀 Gerar Manual"
```

### Opção C: Não Verificar (Rápido)
```
1. Preencher dados
2. Clicar "🚀 Gerar Manual"
3. Pronto! (sem verificação)
```

---

## ✨ Erros Detectados na Escrita

A verificação acontece **ANTES** de gerar o .docx e detecta:

### ✅ Acentuação
```
usuario → usuário
modulo → módulo
funcao → função
acao → ação
```

### ✅ Ortografia
```
proceso → processo
sisitema → sistema
seleçao → seleção
```

### ✅ Verbos
```
clica → clicar
inseri → inserir
```

### ✅ Padrões
```
espaços múltiplos
palavras duplicadas
pontuação dupla
```

---

## 📊 Exemplo Prático

### Passo 1: Preencher Objetivo
```
❌ Objetivo atual:
"Descrever o proceso de edição de trechos musicais no sistema modulo,
permitindo ao usuario criar e classificar conteúdo."
```

### Passo 2: Clicar "Verificar Erros"
```
⚠️ 3 erro(s) encontrado(s):

1. 'proceso' → Sugestão: 'processo'
2. 'modulo' → Sugestão: 'módulo'  
3. 'usuario' → Sugestão: 'usuário'
```

### Passo 3: Escolher Ação

**Opção A - Manual:**
- Editar os campos manualmente
- Corrigir 'processo', 'módulo', 'usuário'

**Opção B - Automática:**
- Clicar "Auto-Corrigir"
- Sistema aplica todas as correções

### Passo 4: Gerar Manual
```
✅ "Gerando manual com texto corrigido..."
📄 Manual_Edição.docx baixado com sucesso
```

---

## ⏱️ Quando Acontece?

| Momento | Ação | Resultado |
|---------|------|-----------|
| **Durante preenchimento** | Você escreve | Sem verificação (você digita normalmente) |
| **Aba "Gerar Manual"** | Clica verificar | Erros são encontrados ⭐ |
| **Aba "Gerar Manual"** | Clica corrigir | Texto é corrigido ⭐ |
| **Ao gerar documento** | Clica "Gerar" | Manual .docx criado com texto final |

---

## 🎨 Interface Streamlit

Na aba **"🚀 Gerar Manual"** você verá:

```
┌─────────────────────────────────────────┐
│ 🔍 Verificação Gramatical (Opcional)   │
│                                         │
│ [✅ Verificar Erros] [🔧 Auto-Corrigir]│
│                                         │
│ (Resultado aparece aqui)                │
│                                         │
├─────────────────────────────────────────┤
│ [🚀 Gerar Manual .docx]                |
└─────────────────────────────────────────┘
```

---

## 💡 Dicas de Uso

### ✅ Recomendado
1. Preencher todos os dados
2. Clicar "Verificar Erros" antes de gerar
3. Revisar sugestões
4. Gerar manual

### ⚠️ Evitar
- Não revisar antes de gerar
- Usar auto-correção sem conhecer o conteúdo
- Gerar documento com muitos erros

### 🚀 Mais Rápido
- Use "Auto-Corrigir" para correções óbvias
- Use "Verificar Erros" para textos técnicos

---

## 📞 F.A.Q.

**P: A correção afeta meus arquivos originais?**  
R: Não! A correção é feita na memória, você pode revisar antes de gerar.

**P: Posso reverter a correção?**  
R: Sim! Edite os campos manualmente antes de gerar.

**P: É obrigatório usar a verificação?**  
R: Não! É totalmente opcional. Você pode gerar sem verificar.

**P: A correção automática sempre está correta?**  
R: Na maioria das vezes sim, mas recomenda-se revisar.

**P: Posso alterar o texto após verificar?**  
R: Sim! Edite os campos na aba "Conteúdo" ou "Funcionalidades" antes de gerar.

---

## 🔄 Resumo

| Parte | O que faz | Quando |
|-------|-----------|--------|
| **Verificar Erros** | Mostra problemas | Antes de gerar |
| **Auto-Corrigir** | Corrige automaticamente | Antes de gerar |
| **Gerar Manual** | Cria arquivo .docx | Após revisar |

🎯 **O fluxo é: Preencher → Verificar → Corrigir → Gerar**
