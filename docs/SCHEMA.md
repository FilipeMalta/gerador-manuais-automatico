# Schema de Dados

## Entrada (manual_input.json)

```json
{
  "nome_produto": "string - Nome do produto",
  "descricao": "string - Descrição breve",
  "versao": "string - Versão semântica",
  "autor": "string - Nome do autor",
  "requisitos": ["string - Lista de requisitos"],
  "funcionalidades": ["string - Lista de funcionalidades"],
  "instrucoes_instalacao": "string - Como instalar",
  "exemplos_uso": [
    {
      "titulo": "string",
      "descricao": "string",
      "codigo": "string"
    }
  ]
}
```

## Validações

- `nome_produto`: Obrigatório, não vazio
- `descricao`: Obrigatório, mínimo 10 caracteres
- `versao`: Formato semântico (X.Y.Z)
- `requisitos`: Array com mínimo 1 item
- `exemplos_uso`: Array com mínimo 1 exemplo

## Saída (Manual em Markdown)

O arquivo gerado será um documento Markdown seguindo o padrão definido em `PADRAO_MANUAL.md`.
