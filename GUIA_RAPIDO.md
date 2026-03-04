# 🚀 Guia Rápido - Gerador de Manuais v2.0

## 5 Minutos para Começar

### 1️⃣ Instalação Rápida
```bash
# Clone o repositório
git clone https://github.com/FilipeMalta/gerador-manuais-automatico.git
cd gerador-manuais-automatico

# Instale as dependências
pip install -r requirements.txt
```

### 2️⃣ Prepare seus Arquivos
Crie uma estrutura de pastas:
```
meu-manual/
├── manual_input.json
├── logo.png
└── screenshots/
    ├── tela1.png
    ├── tela2.png
    └── tela3.png
```

### 3️⃣ Crie o JSON (copie e adapte)
```json
{
  "metadata": {
    "nome_manual": "Manual do Sistema XYZ",
    "modulo": "Módulo Principal",
    "sistema": "Sistema XYZ Completo",
    "elaborado": "10/02/2026",
    "revisado": "10/02/2026",
    "classificacao": "interna",
    "logo_path": "logo.png"
  },
  "objetivo": "Documentar os processos principais do módulo...",
  "pre_requisito": "Usuário com perfil de administrador...",
  "funcionalidades": [
    {
      "titulo": "Primeira Funcionalidade",
      "descricao": "Descrição de como usar...",
      "prints": ["screenshots/tela1.png"],
      "observacoes": [
        "Ponto importante 1",
        "Ponto importante 2"
      ],
      "icones": [
        {
          "nome": "Ícone 1",
          "descricao": "O que esse ícone faz"
        }
      ]
    }
  ]
}
```

### 4️⃣ Gere o Manual
```bash
# Via linha de comando (rápido)
python src/gerador_manual.py meu-manual/manual_input.json saida/Manual.docx

# Via interface web (mais amigável)
python -m streamlit run app.py
```

### 5️⃣ Use o Manual!
Abra o arquivo `.docx` no Word/LibreOffice e aproveite!

---

## 📋 Template JSON Mínimo

Se prefere começar simples (v1.0 compatível):

```json
{
  "metadata": {
    "nome_manual": "Seu Manual",
    "modulo": "Seu Módulo",
    "elaborado": "10/02/2026",
    "revisado": "10/02/2026",
    "classificacao": "interna"
  },
  "objetivo": "Objetivo aqui",
  "pre_requisito": "Pré-requisito aqui",
  "funcionalidades": [
    {
      "titulo": "Funcionalidade 1",
      "descricao": "Descrição aqui",
      "prints": [],
      "observacoes": []
    }
  ]
}
```

---

## 🎯 Checklist para Manual Profissional

- [ ] Metadados preenchidos (nome, módulo, sistema)
- [ ] Datas de elaboração e revisão corretas
- [ ] Classificação apropriada (interna/confidencial/pública)
- [ ] Logo da empresa (arquivo `logo_path`)
- [ ] Objetivo claro e objetivo (2-3 parágrafos)
- [ ] Pré-requisitos bem definidos
- [ ] Funcionalidades em ordem lógica
- [ ] Screenshots com nomes descritivos
- [ ] Observações importantes identificadas
- [ ] Ícones documentados (novo em v2.0!)
- [ ] Validação JSON (use jsonlint.com)

---

## ✨ Recursos Novos (v2.0)

### Breadcrumbs (automático)
```
Módulo >> Funcionalidade
```
Gerado automaticamente baseado no módulo e título da funcionalidade.

### Legendas de Figuras (automático)
```
Figura 3.1.1: Nome da Funcionalidade
```
Numeradas hierarquicamente. Duas imagens = Figura 3.1.1 e Figura 3.1.2

### Campo de Ícones (novo)
```json
"icones": [
  {
    "nome": "Play",
    "descricao": "Inicia a reprodução do áudio"
  }
]
```

### Observações com Bullets (automático)
```
Observações:
• Primeira observação
• Segunda observação
```

---

## 🎨 Exemplo Visual

### Capa Gerada:
```
┌─────────────────────────────────┐
│                                 │
│        [LOGO DA EMPRESA]        │
│                                 │
│                                 │
│   Manual do Sistema XYZ         │
│                                 │
│   Módulo Principal              │
│                                 │
│   Sistema XYZ Completo          │
│                                 │
│   Elaborado: 10/02/2026         │
│   Revisado: 10/02/2026          │
│   Classificação: INTERNA        │
│                                 │
│  ────────────────────────────  │
└─────────────────────────────────┘
```

### Seção de Funcionalidade Gerada:
```
Módulo Principal >> Primeira Funcionalidade

3.1 Primeira Funcionalidade

[Screenshot aqui - Figura 3.1.1]

Descrição de como usar...

Observações:
• Ponto importante 1
• Ponto importante 2

Ícones Utilizados:
• Ícone 1: O que esse ícone faz
```

---

## 🔍 Validação JSON

### Online (recomendado)
1. Acesse https://jsonlint.com/
2. Cole seu JSON
3. Clique em "Validate JSON"
4. Se tiver erros, corrija!

### Localmente (Python)
```python
import json

with open('manual_input.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)
    print("✅ JSON válido!")
```

---

## 📊 Tamanho Recomendado

Para um manual profissional:

| Elemento | Mín | Máx | Ideal |
|----------|-----|-----|-------|
| Funcionalidades | 2 | 15 | 5-8 |
| Observações/func | 0 | 5 | 1-3 |
| Screenshots/func | 0 | 3 | 1-2 |
| Ícones/func | 0 | 10 | 2-5 |

---

## 🛠️ Troubleshooting

### ❌ "Imagem não encontrada"
- Verifique caminhos relativos no JSON
- Use barras `/` não `\`
- Caminho deve ser relativo ao JSON

### ❌ "JSON inválido"
- Verifique vírgulas faltantes
- Use um validador online
- Aspas devem ser retas `"` não curvas

### ❌ "Logo não encontrada"
- Certifique-se de que o arquivo existe
- Caminho deve ser relativo ao `manual_input.json`
- Formatos aceitos: PNG, JPG, JPEG

---

## 📚 Próximos Passos

1. Leia [MELHORIAS_V2.md](MELHORIAS_V2.md) para detalhes completos
2. Consulte [SCHEMA.md](docs/SCHEMA.md) para referência de campos
3. Veja exemplos em `exemplos/input/manual_input.json`
4. Customize conforme sua necessidade!

---

## 💡 Dicas Profissionais

✅ **DO:**
- Use títulos descritivos
- Organize funcionalidades logicamente
- Inclua observações importantes
- Documente ícones principais
- Mantenha linguagem procedural ("Para...", "Clique...")

❌ **DON'T:**
- Use primeira pessoa ("Eu clico...")
- Deixe descrições vagas
- Esqueça datas de elaboração
- Misture idiomas
- Use imagens muito grandes (>5MB)

---

## 🔄 Atualizando de v1.0 para v2.0

Boas notícias: **Totalmente compatível!**

Seus JSONs antigos funcionam perfeitamente. Para aproveitar os novos recursos, basta adicionar:

```json
{
  "titulo": "Funcionalidade",
  "descricao": "...",
  "prints": ["..."],
  "observacoes": ["..."],
  "icones": [
    {
      "nome": "Novo campo",
      "descricao": "Descrição do ícone"
    }
  ]
}
```

O campo `icones` é completamente opcional!

---

## 📞 Precisa de Ajuda?

- 📖 Consulte [SCHEMA.md](docs/SCHEMA.md)
- 📝 Veja exemplos em `exemplos/`
- 🐛 Abra uma issue no GitHub
- 💬 Sugira melhorias!

---

**Versão**: 2.0.0  
**Última Atualização**: 10/02/2026  
**Status**: ✅ Pronto para Uso  

Boa sorte com seu manual! 🎉
