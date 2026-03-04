# 🤖 Gerador Automático de Manuais Word

Sistema profissional de geração automática de manuais técnicos seguindo padrão corporativo internacional.

**Versão**: 2.0.0 | **Status**: ✅ Pronto para Uso | **Última Atualização**: 10/02/2026

## 🎯 Features

### Padrão v2.0 (Profissional)
- ✨ **Breadcrumbs de navegação** automáticos
- 📸 **Legendas de figuras** com numeração hierárquica
- 📄 **Rodapé profissional** com metadados completos
- 🎨 **Capa redesenhada** com informações de sistema
- 🎯 **Documentação de ícones** com descrições
- 📝 **Observações formatadas** em lista com bullets
- 📑 **Sumário automático** com hiperlinks
- 🔄 **Totalmente retrocompatível** com versão 1.0

### Features Gerais
- Interface web para criar manuais facilmente (Streamlit)
- 🔍 **Corretor Gramatical PT-BR** integrado (sem dependências externas)
- Estrutura padronizada (Capa, Sumário, Objetivo, Pré-requisito, Funcionalidades)
- Inserção automática de screenshots
- Schema JSON validado
- Numeração automática de páginas

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

## ✨ Correção Ortográfica (Opcional)

O **Gerador de Manuais** inclui um sistema de correção ortográfica e gramatical integrado, alimentado por **inteligência artificial (LLM)** através do [Ollama](https://ollama.ai/). A correção é **100% local** - seus dados nunca são enviados para servidores externos.

### Como Funciona

- **LLM Local**: Usa o Ollama rodando localmente em sua máquina
- **Modelos Disponíveis**: Mixtral (padrão), Neural-Chat, Mistral, LLaMA 2
- **Privacidade Total**: Todas as correções ocorrem offline em sua máquina
- **Performance**: Configurável (timeout padrão: 30s, máx 2000 chars por chunk)
- **Opcional**: Você decide se quer usar na interface web

### Pré-requisitos

- **Ollama instalado** em sua máquina
- **Modelo LLM** baixado (e.g., Mixtral, Neural-Chat)
- **Dependência Python**: `requests>=2.31.0` (já incluído em `requirements.txt`)

### Instalação do Ollama

#### Windows

1. **Baixar Ollama**: https://ollama.ai/download/windows
2. **Instalar**: Execute o instalador `.exe`
3. **Verificar instalação**:
   ```powershell
   ollama --version
   ```

#### macOS

```bash
# Via Homebrew (recomendado)
brew install ollama

# Ou baixar manualmente em https://ollama.ai/download/mac
```

#### Linux

```bash
# Download e instalação automática
curl https://ollama.ai/install.sh | sh
```

### Baixar Modelo LLM

Por padrão, o sistema usa **Mixtral** (excelente balanço velocidade/qualidade):

```bash
ollama pull mixtral
```

**Alternativas** (escolha uma):

```bash
ollama pull neural-chat    # Otimizado para conversação
ollama pull mistral        # Rápido e preciso
ollama pull llama2         # Modelo base robusto
```

### Iniciar Ollama

Em um terminal, execute:

```bash
ollama serve
```

Você verá uma mensagem como:
```
2026/02/10 15:30:00 Listening on 127.0.0.1:11434 (http)
```

**Deixe este terminal aberto** enquanto usa a aplicação.

### Usando na Interface Web

1. **Inicie a aplicação**:
   ```bash
   python -m streamlit run app.py
   ```

2. **Na aba "Funcionalidades"**:
   - Escreva a descrição da funcionalidade
   - ✅ Marque o checkbox **"✨ Corrigir ortografia automaticamente"**
   - Clique em **"🔍 Pré-visualizar Correção"** para ver o resultado (opcional)
   - Clique em **"➕ Adicionar Funcionalidade"** para salvar com correção aplicada

3. **Na sidebar**:
   - Você verá o status **"🟢 Online"** ou **"🔴 Offline"** do Ollama
   - Se **"🔴 Offline"**: Inicie Ollama com `ollama serve`

### Configuração Avançada

Com **variáveis de ambiente**, você pode personalizar o comportamento:

#### Windows PowerShell

```powershell
# Trocar modelo
$env:OLLAMA_MODEL="neural-chat"

# Aumentar timeout (segundos)
$env:OLLAMA_TIMEOUT="60"

# Iniciar app
python -m streamlit run app.py
```

#### Windows CMD

```cmd
set OLLAMA_MODEL=neural-chat
set OLLAMA_TIMEOUT=60
python -m streamlit run app.py
```

#### Linux / macOS

```bash
export OLLAMA_MODEL=neural-chat
export OLLAMA_TIMEOUT=60
python -m streamlit run app.py
```

**Variáveis disponíveis** (em `src/config.py`):

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | URL do servidor Ollama |
| `OLLAMA_MODEL` | `mixtral` | Modelo LLM a usar |
| `OLLAMA_TIMEOUT` | `30` | Timeout em segundos |
| `MAX_TEXTO_CHUNK` | `2000` | Máx caracteres por requisição |

### Privacidade & Segurança

✅ **100% Local**: Todo processamento ocorre em sua máquina  
✅ **Sem Internet**: Não requer conexão com servidores externos  
✅ **Seus Dados**: Nenhum dado é armazenado ou compartilhado  
✅ **Código Aberto**: Veja [src/correcao_ortografica.py](src/correcao_ortografica.py) para detalhes  

### Troubleshooting

#### ❌ "Ollama não está disponível"

**Problema**: A interface mostra status "🔴 Offline"

**Solução**:
1. Inicie Ollama em um novo terminal: `ollama serve`
2. Verifique se está respondendo: `curl http://localhost:11434/api/tags`
3. Se porta 11434 está ocupada, libere ou altere via variável de ambiente

#### ❌ "Timeout na correção"

**Problema**: Mensagem de erro após clicar em "Pré-visualizar"

**Solução**:
1. Aumentar timeout: `set OLLAMA_TIMEOUT=60` (Windows) ou `export OLLAMA_TIMEOUT=60` (Linux/Mac)
2. Texto muito grande? É automaticamente dividido em chunks (max 2000 chars)
3. Modelo muito grande? Tente: `ollama pull mistral` (mais rápido)

#### ❌ "Modelo não encontrado"

**Problema**: Erro no Ollama indicando modelo não existe

**Solução**:
```bash
# Verificar modelos disponíveis
ollama list

# Baixar modelo faltante
ollama pull mixtral
```

#### ❌ "CUDA/GPU Errors"

**Problema**: Ollama tenta usar GPU e falha

**Solução**:
- Ollama usa GPU automaticamente se disponível
- Se tiver problemas, force CPU: `OLLAMA_CPU_OVERRIDE=true ollama serve`

### Testes da Correção Ortográfica

Para validar que tudo está funcionando, execute os testes:

```bash
# Todos os testes (alguns podem pular se Ollama offline)
pytest tests/ -v

# Apenas testes de integração (requer Ollama)
pytest tests/test_correcao_ortografica.py::TestConexaoOllama -v

# Apenas testes offline (não precisa Ollama)
pytest tests/ -k "Offline or Config or Chunking" -v
```

Veja [tests/README.md](tests/README.md) para detalhes completos.

## 📖 Documentação

- [**MELHORIAS_V2.md**](MELHORIAS_V2.md) - Detalhes completos das novas funcionalidades
- [**SCHEMA.md**](docs/SCHEMA.md) - Documentação completa do JSON (incluindo novos campos)

## 🏗️ Arquitetura

```
Input (JSON + Prints) → Gerador Python (v2.0) → Manual Word (.docx) [Padrão Profissional]
```

### Fluxo Completo

1. **Preparar dados** - JSON estruturado + screenshots + logo (opcional)
2. **Executar gerador** - `python src/gerador_manual.py input.json output.docx`
3. **Obter manual** - Arquivo .docx profissional com todos os recursos

## 📋 Exemplo de JSON (v2.0)

```json
{
  "metadata": {
    "nome_manual": "Manual Sistema X",
    "modulo": "Módulo Y",
    "sistema": "Sistema Completo",
    "elaborado": "03/02/2026",
    "revisado": "03/02/2026",
    "classificacao": "interna",
    "logo_path": "logo.png"
  },
  "objetivo": "Descrever funcionalidades do módulo...",
  "pre_requisito": "Permissões necessárias...",
  "funcionalidades": [
    {
      "titulo": "Tela Principal",
      "descricao": "Interface apresenta...",
      "prints": ["tela.png"],
      "observacoes": ["Obs importante"],
      "icones": [
        {
          "nome": "Play",
          "descricao": "Inicia reprodução"
        }
      ]
    }
  ]
}
```

## 📂 Estrutura do Projeto

```
├── app.py                         # Interface web Streamlit
├── README.md                      # Este arquivo
├── MELHORIAS_V2.md               # Detalhes das melhorias
├── src/
│   ├── gerador_manual.py          # Gerador v2.0 (profissional)
│   ├── schema.py                  # Validação JSON
│   └── prompts/
│       └── prompt_ia.md           # Prompts para IA
├── exemplos/
│   ├── input/
│   │   ├── manual_input.json      # Exemplo de entrada
│   │   ├── logo.png               # Logo de exemplo
│   │   ├── tela_principal.png     # Screenshot exemplo
│   │   └── criar_trecho.png       # Screenshot exemplo
│   └── output/                    # Manuais gerados
└── docs/
    ├── SCHEMA.md                  # Documentação JSON (v2.0)
    └── SCHEMA_LEGADO.md           # Documentação v1.0 (arquivado)
```

## ✨ Novidades da Versão 2.0

### Breadcrumbs de Navegação
Cada funcionalidade exibe navegação hierárquica:
```
Música ao Vivo >> Tela Principal
Música ao Vivo >> Criar Trecho
```

### Legendas Automáticas
Figurasrecebem numeração automática:
```
Figura 3.1.1: Tela Principal
Figura 3.1.2: Tela Principal
```

### Rodapé Profissional
```
Elaborado: 25/01/2026 • Revisado: 03/02/2026 • Classificação: INTERNA • Página 1 de 10
```

### Campo de Ícones
Documenta ícones importantes:
```json
"icones": [
  {
    "nome": "Player",
    "descricao": "Inicia reprodução"
  }
]
```

### Observações Formatadas
```
Observações:
• Primeira observação importante
• Segunda observação importante
```

## 🔄 Retrocompatibilidade

✅ **Totalmente retrocompatível com v1.0**

- JSONs antigos funcionam perfeitamente
- Campo `icones` é totalmente opcional
- Novos recursos funcionam automaticamente

**Migração**: Basta atualizar o `gerador_manual.py` para v2.0

## 🎨 Recursos de Formatação

| Elemento | Tamanho | Cor | Estilo |
|----------|---------|-----|--------|
| Título Manual | 28pt | Cinza escuro | Negrito |
| Subtítulo | 14pt | Cinza | Negrito |
| Rodapé | 8pt | Cinza | Normal |
| Breadcrumbs | 10pt | Azul claro | Itálico |
| Legendas | 9pt | Cinza | Itálico |

## 📊 Exemplos de Saída

### Capa Profissional
```
[LOGO]

Manual Música ao Vivo - Edição

Música ao Vivo

Sistema de Gestão Musical

Elaborado: 25/01/2026
Revisado: 03/02/2026
Classificação: INTERNA

──────────────────────────────────────
```

### Seção de Funcionalidade
```
Música ao Vivo >> Tela Principal
3.1 Tela Principal

[Figura 3.1.1]

Descrição da funcionalidade...

Observações:
• Observação 1
• Observação 2

Ícones Utilizados:
• Play: Inicia reprodução
• Stop: Para reprodução
```

## 🎯 Roadmap

- [x] Gerador base funcional
- [x] Schema JSON validado
- [x] Interface web (Streamlit)
- [x] **Padrão profissional v2.0**
- [x] **Dokumentação completa**
- [ ] API REST
- [ ] Playwright para screenshots automáticos
- [ ] Geração em PDF
- [ ] Múltiplos idiomas

## 🤝 Contribuindo

PRs são bem-vindos! Para mudanças maiores, abra uma issue primeiro.

## 📝 Licença

MIT

## 👤 Autor

**Filipe Malta Perfeito**  
Desenvolvedor | Documentação Técnica | Sistemas de Automação

---

## 📚 Documentação Adicional

- [MELHORIAS_V2.md](MELHORIAS_V2.md) - Guia completo das novas funcionalidades
- [SCHEMA.md](docs/SCHEMA.md) - Referência detalhada de campos JSON
- [exemplos/](exemplos/) - Arquivos de exemplo

---

⭐ Se este projeto foi útil, deixe uma estrela!
