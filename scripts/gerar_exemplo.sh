#!/bin/bash

# Script para gerar um exemplo de manual

echo "Gerando exemplo de manual..."

# Verifica se o arquivo de entrada existe
if [ ! -f "exemplos/input/manual_input.json" ]; then
    echo "Erro: Arquivo de entrada não encontrado!"
    exit 1
fi

# Executa o gerador
python src/gerador_manual.py \
    --input exemplos/input/manual_input.json \
    --output exemplos/output/manual_gerado.md

# Verifica se foi gerado com sucesso
if [ -f "exemplos/output/manual_gerado.md" ]; then
    echo "✓ Manual gerado com sucesso em: exemplos/output/manual_gerado.md"
else
    echo "✗ Erro ao gerar o manual"
    exit 1
fi
