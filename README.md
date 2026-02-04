# 🤖 Gerador Automático de Manuais Word

Sistema profissional de geração automática de manuais técnicos seguindo padrão corporativo.

## 🎯 Features

- Interface web para criar manuais facilmente
- Estrutura padronizada (Capa, Sumario, Objetivo, Pre-requisito, Funcionalidades)
- Rodape automatico com numeracao de paginas
- Insercao automatica de screenshots
- Observacoes numeradas
- Schema JSON validado  

## 🚀 Quick Start

### Instalação

```bash
git clone https://github.com/FilipeMalta/gerador-manuais-automatico.git
cd gerador-manuais-automatico
pip install -r requirements.txt
```

### Interface Web (Recomendado)

```bash
python -m streamlit run app.py
```
Acesse http://localhost:8501 no navegador.

### Linha de Comando

```bash
python src/gerador_manual.py exemplos/input/manual_input.json exemplos/output/MeuManual.docx
```

## 📖 Documentação

- [Schema JSON](docs/SCHEMA.md)

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

## 📂 Estrutura do Projeto

```
├── app.py                     # Interface web Streamlit
├── src/
│   ├── gerador_manual.py      # Gerador principal
│   └── schema.py              # Validação JSON
├── exemplos/
│   ├── input/                 # Exemplos de entrada
│   └── output/                # Manuais gerados
└── docs/
    └── SCHEMA.md              # Documentacao do JSON
```

## 🎯 Roadmap

- [x] Gerador base funcional
- [x] Schema JSON validado
- [x] Interface web (Streamlit)
- [ ] API REST
- [ ] Playwright para screenshots automáticos

## 🤝 Contribuindo

PRs são bem-vindos! Para mudanças maiores, abra uma issue primeiro.

## 📝 Licença

MIT

## 👤 Autor

**Filipe Malta Perfeito**

---

⭐ Se este projeto foi útil, deixe uma estrela!