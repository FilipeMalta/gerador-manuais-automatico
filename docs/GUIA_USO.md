# Guia de Uso - Gerador de Manuais Automático

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd gerador-manuais-automatico
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

## Uso Básico

### Executar o gerador:

```bash
python src/gerador_manual.py --input exemplos/input/manual_input.json --output exemplos/output/manual.md
```

### Argumentos:

- `--input`: Caminho do arquivo JSON de entrada
- `--output`: Caminho do arquivo Markdown de saída
- `--template`: Template customizado (opcional)

## Exemplo de Entrada

Veja `exemplos/input/manual_input.json` para um exemplo completo.

## Saída

O arquivo gerado em `exemplos/output/` será um manual completo em Markdown pronto para publicação.

## Troubleshooting

Se encontrar erros, consulte a documentação em `docs/`.
