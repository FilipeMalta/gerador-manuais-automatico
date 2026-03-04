# Testes do Gerador de Manuais Automático

Testes automatizados para o módulo de correção ortográfica com Ollama.

## 📋 Estrutura dos Testes

```
tests/
├── __init__.py                    # Marca diretório como pacote Python
├── conftest.py                    # Configuração do pytest (fixtures globais)
└── test_correcao_ortografica.py  # Testes unitários
```

## 🚀 Como Executar

### Pré-requisitos

1. **Instalar dependências de teste:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Para testes que precisam Ollama:**
   ```bash
   ollama serve
   ```
   (em outro terminal)

### Executar Todos os Testes

```bash
# Verbose (detalhado)
pytest tests/ -v

# Com cobertura
pytest tests/ --cov=src --cov-report=html
```

### Executar Teste Específico

```bash
# Por classe
pytest tests/test_correcao_ortografica.py::TestConexaoOllama -v

# Por função
pytest tests/test_correcao_ortografica.py::TestConexaoOllama::test_conexao_ollama_disponivel -v

# Por padrão de nome
pytest tests/ -k "test_correcao_simples" -v
```

### Executar Apenas Testes Unit (Sem Ollama)

```bash
# Apenas mocks (não precisa Ollama rodando)
pytest tests/ -k "Offline or Config or Chunking" -v
```

### Executar Apenas Testes de Integração (Com Ollama)

```bash
# Testes que precisam Ollama
pytest tests/test_correcao_ortografica.py::TestConexaoOllama -v
pytest tests/test_correcao_ortografica.py::TestCorrecaoSimples -v
pytest tests/test_correcao_ortografica.py::TestTextoSemErro -v
```

## 📝 Descrição dos Testes

### `TestConexaoOllama`
Testes de conectividade com servidor Ollama.

| Teste | Propósito | Depende de Ollama |
|-------|----------|-------------------|
| `test_conexao_ollama_disponivel` | Verifica se consegue conectar ao Ollama | ✅ Sim |
| `test_config_padrao` | Valida carregamento de configurações | ❌ Não |

**Resultado esperado:**
- Se Ollama não está disponível: teste é pulado (skipped) com mensagem
- Se disponível: conecta e valida configurações padrão

### `TestCorrecaoSimples`
Testes de correção de textos com erros ortográficos.

| Teste | Input | Expected | Depende de Ollama |
|-------|-------|----------|-------------------|
| `test_correcao_erro_basico` | "Eu preçiso ajuda" | "Eu preciso ajuda" | ✅ Sim |
| `test_correcao_multiplos_erros` | Texto com 3+ erros | Erros corrigidos | ✅ Sim |

**Resultado esperado:**
- Texto corrigido contém as palavras corrigidas
- Nenhuma exceção lançada

### `TestTextoSemErro`
Testes com entradas especiais e boas.

| Teste | Input | Comportamento Esperado | Depende de Ollama |
|-------|-------|----------------------|-------------------|
| `test_texto_correto_nao_muda` | Texto sem erros | Mantém palavras-chave | ✅ Sim |
| `test_texto_vazio` | `""` | Retorna string válida | ✅ Sim |
| `test_texto_apenas_espacos` | `"   "` | Retorna string válida | ✅ Sim |

### `TestOllamaOffline`
Testes de comportamento quando Ollama não está disponível (usa mock).

| Teste | Simula | Comportamento Esperado | Depende de Ollama |
|-------|--------|----------------------|-------------------|
| `test_verificar_disponibilidade_offline` | ConnectionError | Retorna False | ❌ Não (mock) |
| `test_corrigir_com_timeout` | Timeout | Retorna texto original | ❌ Não (mock) |
| `test_corrigir_com_erro_conexao` | ConnectionError | Retorna texto original | ❌ Não (mock) |
| `test_offline_verificacao_com_mock` | ConnectionError | Retorna False | ❌ Não (mock) |

**Importante:** Estes testes usam `unittest.mock` para simular erros, então não precisam Ollama.

### `TestIntegrationConfig`
Testes de integração com sistema de configuração.

| Teste | Propósito | Depende de Ollama |
|-------|----------|-------------------|
| `test_variables_ambiente_nao_carregam_durante_test` | Valida estrutura de config | ❌ Não |
| `test_corretor_usa_config_padrao` | Verifica valores padrão | ❌ Não |

### `TestChunking`
Testes de divisão de textos grandes em chunks.

| Teste | Input Size | Comportamento Esperado | Depende de Ollama |
|-------|-----------|----------------------|-------------------|
| `test_dividir_texto_pequeno` | < 2000 chars | Sem divisão (1 chunk) | ❌ Não |
| `test_dividir_texto_grande` | > 2000 chars | Múltiplos chunks | ❌ Não |

## 🔧 Configuração

### arquivo: `pytest.ini`
Define configurações globais de testes:
- Diretório de testes: `tests/`
- Padrão de nomes: `test_*.py`, `Test*`, `test_*`
- Saída verbosa por padrão
- Desabilita avisos desnecessários

### arquivo: `conftest.py`
Configura fixtures e hooks do pytest:
- Carrega automaticamente diretório raiz ao path
- Define markers personalizados (`@pytest.mark.integration`, `@pytest.mark.unit`)

## 📊 Exemplo de Saída

Ao executar sem Ollama disponível:

```
tests/test_correcao_ortografica.py::TestConexaoOllama::test_conexao_ollama_disponivel SKIPPED
❌ Ollama não está disponível em http://localhost:11434. Inicie Ollama com: ollama serve

tests/test_correcao_ortografica.py::TestConexaoOllama::test_config_padrao PASSED
tests/test_correcao_ortografica.py::TestOllamaOffline::test_verificar_disponibilidade_offline PASSED
tests/test_correcao_ortografica.py::TestChunking::test_dividir_texto_pequeno PASSED
...

====== 5 passed, 3 skipped in 0.23s ======
```

Ao executar COM Ollama disponível:

```
tests/test_correcao_ortografica.py::TestConexaoOllama::test_conexao_ollama_disponivel PASSED
tests/test_correcao_ortografica.py::TestConexaoOllama::test_config_padrao PASSED
tests/test_correcao_ortografica.py::TestCorrecaoSimples::test_correcao_erro_basico PASSED
tests/test_correcao_ortografica.py::TestCorrecaoSimples::test_correcao_multiplos_erros PASSED
tests/test_correcao_ortografica.py::TestTextoSemErro::test_texto_correto_nao_muda PASSED
...

====== 14 passed, 1 skipped in 2.45s ======
```

## 💡 Dicas de Debugging

### Ver logs durante teste
```bash
pytest tests/ -v --log-cli-level=DEBUG
```

### Ver apenas testes que falharam
```bash
pytest tests/ -v --lf
```

### Parar no primeiro erro
```bash
pytest tests/ -v -x
```

### Rodar comTestamento específico mais lentamente
```bash
pytest tests/test_correcao_ortografica.py::TestCorrecaoSimples::test_correcao_erro_basico -v -s
```

## 🤖 Requisitos para Testes de Integração

Para testes que dependem de Ollama (`TestConexaoOllama`, `TestCorrecaoSimples`, `TestTextoSemErro`):

1. **Instalação do Ollama:** https://ollama.ai/
2. **Modelo carregado:**
   ```bash
   ollama pull mixtral  # Ou outro modelo
   ```
3. **Servidor rodando:**
   ```bash
   ollama serve
   ```
4. **Available em:** `http://localhost:11434`

Se Ollama não estiver disponível, esses testes serão automaticamente pulados com mensagem clara.

## 📦 Dependências de Teste

```
pytest >= 7.0.0
```

Já incluído em `requirements.txt`.

## ✅ Checklist de Execução

- [ ] `pip install -r requirements.txt` - Instalar dependências
- [ ] `ollama serve` - Iniciar Ollama (em outro terminal, se quiser testar integração)
- [ ] `pytest tests/ -v` - Executar todos os testes
- [ ] Verificar que testes offline passam mesmo sem Ollama
- [ ] Verificar que testes de integração passam com Ollama
- [ ] Revisar relatório de cobertura: `pytest tests/ --cov=src --cov-report=html`
