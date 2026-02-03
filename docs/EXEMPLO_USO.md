# 📖 Exemplo Completo de Uso

Guia prático passo a passo para gerar um manual automaticamente.

---

## 📋 Passo 1: Preparar Entrada (JSON)

Crie um arquivo `manual_input.json` na pasta `exemplos/input/` com a estrutura abaixo:

```json
{
  "metadata": {
    "nome_manual": "Manual Música ao Vivo - Edição",
    "modulo": "Música ao Vivo",
    "sistema": "Sistema XYZ",
    "elaborado": "25/01/2026",
    "revisado": "03/02/2026",
    "classificacao": "interna",
    "logo_path": "logo.png"
  },
  "objetivo": "Descrever o processo de edição de trechos musicais, permitindo criar, classificar e gerenciar segmentos de áudio.",
  "pre_requisito": "Usuário com perfil de Editor cadastrado e permissão de acesso ao módulo Música ao Vivo.",
  "funcionalidades": [
    {
      "titulo": "Tela Principal",
      "descricao": "A tela principal apresenta o wave de áudio completo, com barra de ferramentas superior contendo os botões de ação (Criar, Classificar, Remover, Salvar, Voltar, Finalizar).",
      "prints": ["tela_principal.png"],
      "observacoes": []
    },
    {
      "titulo": "Criar Trecho",
      "descricao": "Para criar um trecho, o usuário deve clicar com o mouse na posição inicial do wave e arrastar até a posição final desejada. Ao soltar o botão, o sistema destaca visualmente o trecho selecionado com cor azul claro.",
      "prints": ["criar_trecho.png"],
      "observacoes": [
        "Só após clicar no botão 'Criar Trecho' é que o usuário consegue interagir com o Wave.",
        "Ao criar um trecho sem finalizar (salvar), o sistema mantém como cadastro pendente."
      ]
    },
    {
      "titulo": "Classificar",
      "descricao": "Para classificar um trecho já criado, selecione o trecho clicando sobre ele e em seguida clique no botão 'Classificar'. O sistema exibe uma janela modal com as categorias disponíveis. Ao selecionar uma categoria, o trecho recebe uma etiqueta visual.",
      "prints": ["classificar_trecho.png"],
      "observacoes": [
        "Classificação só está disponível para trechos já criados."
      ]
    }
  ]
}
```

### Checklist de Entrada:
- ✅ Todos os campos obrigatórios preenchidos
- ✅ Datas em formato DD/MM/AAAA
- ✅ Funcionalidades com título e descrição
- ✅ Caminhos de imagens corretos (relativos à pasta do JSON)

---

## 📁 Passo 2: Preparar Arquivos

Organize seus arquivos assim:

```
exemplos/input/
├── manual_input.json          # Seu JSON
├── logo.png                   # Logo da empresa (opcional)
├── tela_principal.png         # Screenshot 1
├── criar_trecho.png           # Screenshot 2
└── classificar_trecho.png     # Screenshot 3
```

**Notas sobre imagens:**
- Formato: PNG, JPG, JPEG
- Tamanho recomendado: 1920x1080 px
- Qualidade: mínimo 72 dpi
- Nome: descritivo e em minúsculas com underscore

---

## 🚀 Passo 3: Executar Gerador

### Via Terminal (Recomendado)

```bash
# Navegue até a pasta do projeto
cd c:\Users\Aluga.com\gerador-manuais-automatico

# Execute o gerador
python src/gerador_manual.py exemplos/input/manual_input.json exemplos/output/Manual_Musica.docx
```

### Saída Esperada:
```
✅ Manual gerado com sucesso: exemplos/output/Manual_Musica.docx
```

---

## 📄 Passo 4: Verificar Saída

O arquivo `Manual_Musica.docx` será gerado com:

### Estrutura Automática:
1. **Capa**
   - Logo (se fornecida)
   - Título do manual
   - Nome do módulo
   
2. **Sumário**
   - Placeholder (atualizar manualmente no Word)
   
3. **Objetivo**
   - Texto descritivo do propósito
   
4. **Pré-requisito**
   - Permissões e configurações necessárias
   
5. **Funcionalidades**
   - Subtítulos numerados (3.1, 3.2, 3.3...)
   - Screenshots centralizados
   - Descrições técnicas
   - Observações numeradas (Obs1, Obs2...)
   
6. **Rodapé em Todas as Páginas**
   - Datas de elaboração e revisão
   - Classificação
   - Numeração automática de páginas (Página X de Y)

---

## ⚠️ Troubleshooting

### Erro: "Arquivo não encontrado"
```
❌ Erro: [Errno 2] No such file or directory: 'exemplos/input/manual_input.json'
```
**Solução:** Verifique o caminho do JSON e o diretório correto.

### Erro: "JSON inválido"
```
❌ Erro: JSON inválido em exemplos/input/manual_input.json
```
**Solução:** Use [JSONLint](https://jsonlint.com/) para validar sintaxe.

### Imagem não encontrada no manual
```
⚠️ Erro ao inserir imagem tela_principal.png: [Errno 2] No such file
[Imagem não encontrada: tela_principal.png]
```
**Solução:** Verifique se a imagem está na mesma pasta do JSON com o nome exato.

---

## 💡 Dicas de Produtividade

### 1. Use IA para Gerar JSON
Copie o prompt em `src/prompts/prompt_ia.md` e use com ChatGPT/Claude:
- Forneça screenshots
- Descreva as regras de negócio
- Deixe a IA gerar o JSON estruturado

### 2. Template Rápido
Copie o JSON de exemplo acima e customize:
```bash
cp exemplos/input/manual_input.json exemplos/input/seu_manual.json
# Edite seu_manual.json
python src/gerador_manual.py exemplos/input/seu_manual.json exemplos/output/seu_manual.docx
```

### 3. Batch Processing
Para múltiplos manuais, crie um script em lote:
```bash
python src/gerador_manual.py exemplos/input/manual1.json exemplos/output/manual1.docx
python src/gerador_manual.py exemplos/input/manual2.json exemplos/output/manual2.docx
python src/gerador_manual.py exemplos/input/manual3.json exemplos/output/manual3.docx
```

---

## 📊 Validação Rápida

Antes de executar, valide seu JSON:

```bash
# Online: https://jsonlint.com/

# Ou via Python:
python -c "import json; json.load(open('exemplos/input/manual_input.json'))"
```

Se não houver erro, o JSON está correto! ✅

---

## 🎯 Próximos Passos

Após gerar o manual Word:

1. ✅ Abrir em Microsoft Word ou LibreOffice
2. ✅ Atualizar Sumário (Clique direito → Atualizar campo)
3. ✅ Revisar formatação e conteúdo
4. ✅ Adicionar assinaturas/aprovações conforme necessário
5. ✅ Exportar para PDF se desejado
6. ✅ Distribuir para stakeholders

---

## 📞 Suporte

Para dúvidas sobre:
- **Schema JSON**: veja [SCHEMA.md](SCHEMA.md)
- **Padrão de Manual**: veja [PADRAO_MANUAL.md](PADRAO_MANUAL.md)
- **Gerador Python**: veja comentários em [gerador_manual.py](../src/gerador_manual.py)
- **Prompt IA**: veja [prompt_ia.md](../src/prompts/prompt_ia.md)

