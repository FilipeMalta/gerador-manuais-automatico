# 🤖 Gerador Automático de Manuais Word

Sistema profissional de geração automática de manuais técnicos seguindo padrão corporativo.

## 🎯 Features

✅ Estrutura padronizada (Capa, Sumário, Objetivo, Pré-requisito, Funcionalidades)  
✅ Rodapé automático com numeração de páginas  
✅ Inserção automática de screenshots  
✅ Observações numeradas  
✅ Schema JSON validado  
✅ Prompt para IA incluído  
✅ Exemplo funcional completo  

## 🚀 Quick Start

### Instalação

```bash
git clone https://github.com/FilipeMalta/gerador-manuais-automatico.git
cd gerador-manuais-automatico
pip install -r requirements.txt
```

### Uso Básico

```bash
python src/gerador_manual.py exemplos/input/manual_input.json exemplos/output/MeuManual.docx
```

## 📖 Documentação

- [Padrão do Manual](docs/PADRAO_MANUAL.md)
- [Schema JSON](docs/SCHEMA.md)
- [Guia de Uso Completo](docs/GUIA_USO.md)

## 🏗️ Arquitetura

```
Input (JSON + Prints) → Gerador Python → Manual Word (.docx)
```

### Fluxo Completo

1. **Preparar dados** - JSON estruturado + screenshots
2. **Executar gerador** - `python src/gerador_manual.py input.json output.docx`
3. **Obter manual** - Arquivo .docx pronto e padronizado

## 📋 Exemplo de JSON

```json
{
  "metadata": {
    "nome_manual": "Manual Sistema X",
    "modulo": "Módulo Y",
    "elaborado": "03/02/2026",
    "revisado": "03/02/2026",
    "classificacao": "interna"
  },
  "objetivo": "Descrever funcionalidades...",
  "pre_requisito": "Permissões necessárias...",
  "funcionalidades": [
    {
      "titulo": "Tela Principal",
      "descricao": "Interface apresenta...",
      "prints": ["tela.png"],
      "observacoes": ["Obs importante"]
    }
  ]
}
```

## 🤖 Uso com IA (Opcional)

Use o prompt em `src/prompts/prompt_ia.md` com ChatGPT/Claude para gerar o JSON automaticamente a partir de screenshots e regras de negócio.

## 🛠️ Tecnologias

- Python 3.8+
- python-docx
- JSON Schema

## 📂 Estrutura do Projeto

```
├── src/
│   ├── gerador_manual.py      # Gerador principal
│   ├── schema.py              # Validação JSON
│   └── prompts/
│       └── prompt_ia.md       # Prompt para IA
├── exemplos/
│   ├── input/                 # Exemplos de entrada
│   └── output/                # Manuais gerados
├── docs/                      # Documentação completa
└── scripts/                   # Scripts auxiliares
```

## 🎯 Roadmap

- [x] Gerador base funcional
- [x] Documentação completa
- [x] Prompt para IA
- [ ] Interface web (Streamlit)
- [ ] API REST
- [ ] Integração CI/CD
- [ ] Playwright para screenshots automáticos

## 🤝 Contribuindo

PRs são bem-vindos! Para mudanças maiores, abra uma issue primeiro.

## 📝 Licença

MIT

## 👤 Autor

**Filipe Malta Perfeito**

---

⭐ Se este projeto foi útil, deixe uma estrela!