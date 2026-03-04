# 📋 Sistema de Logging - Gerador de Manuais

## 📝 Visão Geral

O Gerador de Manuais inclui um **sistema centralizado de logging** que registra todas as operações importantes da aplicação, especialmente:

- 🤖 **Correção Ortográfica**: Quando é usada, qual modelo, tempo de resposta
- 🔌 **Conexão**: Status do Ollama (Online/Offline), tentativas de conexão
- ⏱️ **Performance**: Tempo de resposta, tamanho dos textos processados
- ❌ **Erros**: Todas as exceções e problemas
- 📊 **Operações**: Funcionalidades adicionadas, manuais gerados

## 📂 Arquivo de Logs

```
gerador-manuais-automatico/
└── logs/
    └── app.log          # Arquivo principal de logs
```

**Localização**: `logs/app.log`  
**Tamanho máximo**: 5 MB por arquivo (rotação automática)  
**Backups**: Até 5 cópias antigas (app.log.1, app.log.2, etc.)  
**Encoding**: UTF-8

## 📜 Formato do Log

```
2026-02-10 21:30:44 | INFO     | correcao_ortografica | CorretorOrtografico inicializado | modelo=mixtral | url=http://localhost:11434 | timeout=30s
```

**Componentes:**
- `2026-02-10 21:30:44` - **Timestamp** (YYYY-MM-DD HH:MM:SS)
- `INFO` - **Nível**: DEBUG, INFO, WARNING, ERROR
- `correcao_ortografica` - **Módulo** (arquivo .py)
- Restante - **Mensagem** com detalhes

## 🎯 Tipos de Logs Registrados

### 🤖 Correção Ortográfica

```
CorretorOrtografico inicializado | modelo=mixtral | url=http://localhost:11434 | timeout=30s
✅ Ollama disponível (modelo: mixtral)
⚠️ Modelo 'mixtral' não encontrado. Modelos disponíveis: ['llama2']
Enviando 1234 caracteres para mixtral
✅ Correção concluída | tempo=2.34s | modelo=mixtral | chars=1234
```

### 🔌 Conexão & Status

```
Verificando disponibilidade de http://localhost:11434
Status Ollama: Online
❌ Não consegui conectar a http://localhost:11434
   Certifique-se de que Ollama está rodando:
   Execute: ollama serve
```

### 📝 Funcionalidades

```
Funcionalidade adicionada | titulo='Criar Trecho' | descricao_chars=234 | corrigido=True | modelo=mixtral | prints=2 | obs=1
Pré-visualização de correção acionada | modelo=mixtral | tamanho=234 chars
Pré-visualização concluída | modelo=mixtral | alterações=True
```

### 📊 Geração de Manuais

```
Iniciando geração de manual | nome='Manual Sistema X' | modulo='Módulo Y' | funcionalidades=5
Manual gerado com sucesso | tamanho=125456 bytes | arquivo='Manual_Módulo_Y.docx'
```

### ❌ Erros

```
ERROR | Erro ao corrigir: Connection timeout
ERROR | Perdeu conexão com Ollama durante correção
ERROR | Erro ao gerar manual: File not found
WARNING | Tentativa de adicionar funcionalidade sem título ou descrição
```

## 🔍 Como Analisar Logs

### Ver Logs em Tempo Real

```bash
# Linux/Mac
tail -f logs/app.log

# Windows PowerShell
Get-Content logs/app.log -Wait

# Windows CMD
type logs/app.log  (uma única vez)
```

### Filtrar por Tipo

```bash
# Apenas erros
grep "ERROR" logs/app.log

# Apenas INFO (excluir DEBUG)
grep "INFO\|WARNING\|ERROR" logs/app.log

# Apenas correções
grep "Correção\|Corretor" logs/app.log
```

### Análise de Performance

```bash
# Tempos de resposta do Ollama
grep "Correção concluída" logs/app.log

# Exemplo de saída:
# 2026-02-10 21:30:44 | INFO | correcao_ortografica | ✅ Correção concluída | tempo=2.34s | modelo=mixtral | chars=1234
```

### Contar Operações

```bash
# Quantos manuais foram gerados
grep "Manual gerado com sucesso" logs/app.log | wc -l

# Quantas funcionalidades foram adicionadas
grep "Funcionalidade adicionada" logs/app.log | wc -l
```

## 🛠️ Usar Logger no Seu Código

### Importar

```python
from src.logger import get_logger

logger = get_logger(__name__)
```

### Registrar Mensagens

```python
# Informação
logger.info("Operação concluída com sucesso")

# Aviso
logger.warning("Configuração padrão será usada")

# Erro
logger.error("Falha ao conectar ao servidor")

# Debug (detalhe)
logger.debug("Valor da variável: x = 123")
```

### Registrar Dados Estruturados

```python
# Bom formato para logs
logger.info(f"Operação concluída | tempo={tempo}s | modelo={modelo} | chars={tamanho}")

# Ruim (sem estrutura)
logger.info(f"Operação concluída em {tempo} segundos com o modelo {modelo}")
```

## ⚙️ Configuração

### Localização do Arquivo

Definido em `src/logger.py`:
```python
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOGS_DIR / "app.log"
```

### Nível Padrão

```python
# Arquivo (logs/app.log)
Nível: DEBUG (registra TUDO)

# Console (tela)
Nível: WARNING (mostra apenas WARNING e ERROR)
```

### Ativar Debug no Console

Para ver mensagens DEBUG também na tela:

```python
from src.logger import set_debug_mode

set_debug_mode(True)
logger = get_logger(__name__)
logger.debug("Esta mensagem aparecerá no console")
```

## 📊 Exemplos Reais

### Exemplo 1: Correção Bem-Sucedida

```
2026-02-10 21:30:45 | INFO  | app | Corretor Ortográfico inicializado
2026-02-10 21:30:45 | INFO  | correcao_ortografica | CorretorOrtografico inicializado | modelo=mixtral | url=http://localhost:11434 | timeout=30s
2026-02-10 21:30:45 | INFO  | correcao_ortografica | Verificando disponibilidade de http://localhost:11434
2026-02-10 21:30:45 | INFO  | correcao_ortografica | ✅ Ollama disponível (modelo: mixtral)
2026-02-10 21:30:45 | INFO  | app | Status Ollama: Online
2026-02-10 21:30:50 | INFO  | app | Pré-visualização de correção acionada | modelo=mixtral | tamanho=345 chars
2026-02-10 21:30:50 | INFO  | correcao_ortografica | Enviando 345 caracteres para mixtral
2026-02-10 21:30:52 | INFO  | correcao_ortografica | ✅ Correção concluída | tempo=2.15s | modelo=mixtral | chars=345
2026-02-10 21:30:52 | INFO  | app | Pré-visualização concluída | modelo=mixtral | alterações=True
2026-02-10 21:30:55 | INFO  | app | Funcionalidade adicionada | titulo='Criar Usuário' | descricao_chars=345 | corrigido=True | modelo=mixtral | prints=2 | obs=0
```

### Exemplo 2: Ollama Offline

```
2026-02-10 21:30:45 | INFO  | correcao_ortografica | Verificando disponibilidade de http://localhost:11434
2026-02-10 21:30:48 | ERROR | correcao_ortografica | ❌ Não consegui conectar a http://localhost:11434
   Certifique-se de que Ollama está rodando:
   Execute: ollama serve
2026-02-10 21:30:48 | INFO  | app | Status Ollama: Offline
```

### Exemplo 3: Manual Gerado

```
2026-02-10 21:35:00 | INFO | app | Iniciando geração de manual | nome='Manual Sistema X' | modulo='Módulo Y' | funcionalidades=5
2026-02-10 21:35:10 | INFO | app | Manual gerado com sucesso | tamanho=256789 bytes | arquivo='Manual_Módulo_Y.docx'
```

## 🔐 Privacidade & Segurança

✅ **Logs Locais**: Todos os logs ficam no seu computador  
✅ **Sem Dados Sensíveis**: Não registra senhas ou dados pessoais  
✅ **Leitura Fácil**: Formato texto simples, sem criptografia  
⚠️ **Arquivo Público**: Qualquer um com acesso ao PC pode ler os logs  

## 🧹 Limpiar Logs Antigos

```bash
# Linux/Mac - Remover arquivo de log antigo
rm logs/app.log

# Windows PowerShell
Remove-Item logs/app.log

# Windows CMD
del logs\app.log
```

A próxima execução criará um novo arquivo automaticamente.

## 📈 Monitoramento

Para monitorar em tempo real:

```bash
# Terminal 1: Iniciar Ollama
ollama serve

# Terminal 2: Ver logs em tempo real
tail -f logs/app.log

# Terminal 3: Executar aplicação
python -m streamlit run app.py
```

Você verá os logs aparecerem em tempo real no Terminal 2!

## 📚 Referência Rápida

| Função | Uso |
|--------|-----|
| `logger.debug()` | Detalhes técnicos para debugging |
| `logger.info()` | Informações normais de operação |
| `logger.warning()` | Algo anormal, mas app continua |
| `logger.error()` | Erro que afeta funcionamento |

| Nível | Console | Arquivo |
|-------|---------|---------|
| DEBUG | ❌ Não | ✅ Sim |
| INFO | ❌ Não | ✅ Sim |
| WARNING | ✅ Sim | ✅ Sim |
| ERROR | ✅ Sim | ✅ Sim |

---

**Arquivo**: `src/logger.py`  
**Testado em**: Windows 10/11, Linux, macOS  
**Última atualização**: 10/02/2026
