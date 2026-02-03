# 📘 Padrão de Manual Corporativo

## Estrutura Obrigatória

Todo manual gerado deve seguir esta estrutura fixa:

### 1. Capa
- Logo da empresa (centralizado, topo)
- Título do manual (centralizado, fonte 24pt, negrito)
- Nome do módulo (centralizado, fonte 16pt, cinza)

### 2. Sumário
- Título "Sumário"
- Listagem automática de seções
- Numeração de páginas

### 3. Seção 1: Objetivo
- Descrição clara e concisa do propósito do módulo
- 1-2 parágrafos
- Linguagem objetiva

### 4. Seção 2: Pré-requisito
- Permissões necessárias
- Acessos requeridos
- Configurações prévias
- Dependências de outros módulos

### 5. Seção 3: Funcionalidade
Subdividida em:

#### 3.1 Tela
- Descrição geral da interface
- Elementos principais
- Layout e organização

#### 3.2 Operacionalidade
Subseções para cada ação:
- **Criar**: Como criar novos registros
- **Classificar**: Como categorizar
- **Remover**: Como excluir
- **Salvar**: Como persistir alterações
- **Voltar**: Navegação
- **Finalizar**: Conclusão de processos
- *Outras ações específicas do módulo*

### 6. Rodapé (todas as páginas)
```
Elaborado: DD/MM/AAAA • Revisado: DD/MM/AAAA • Classificação: interna • Página X de Y
```

---

## Estilo de Escrita

### ✅ FAZER
- Usar linguagem procedural: "Ao clicar...", "O sistema...", "Para..."
- Ser específico e técnico
- Referenciar elementos visuais: "botão azul", "campo superior direito"
- Numerar observações: Obs1, Obs2, Obs3...
- Usar voz ativa

### ❌ EVITAR
- Primeira pessoa (eu, nós)
- Linguagem informal ou coloquial
- Ambiguidade ("talvez", "pode ser que")
- Suposições sem base nos prints
- Termos genéricos ("aqui", "ali", "isso")

---

## Observações (Obs)

Use observações para:
- ⚠️ Alertas importantes
- 🔒 Restrições de acesso ou permissão
- 🐛 Comportamentos não óbvios
- 💡 Dicas de uso
- ⏱️ Informações sobre timing ou sequência

**Formato:**
```
Obs1: [Texto da observação]
Obs2: [Texto da observação]
```

---

## Screenshots

### Quando incluir
- Uma por funcionalidade principal
- Em pontos de decisão do usuário
- Para clarificar elementos visuais complexos

### Como incluir
- Sempre após o título da funcionalidade
- Centralizados
- Largura padronizada (5.5 polegadas)
- Com legenda se necessário

### Nomenclatura de arquivos
```
[modulo]_[funcionalidade]_[variacao].png

Exemplos:
musica_tela_principal.png
musica_criar_trecho.png
musica_classificar_modal.png
```

---

## Formatação Visual

### Hierarquia de Títulos
```
# 1. Título Nível 1 (Heading 1)
## 1.1 Título Nível 2 (Heading 2)
### 1.1.1 Título Nível 3 (Heading 3)
```

### Ênfases
- **Negrito**: Termos técnicos importantes, nomes de botões
- *Itálico*: Raramente usado, apenas para citações
- `Código`: Valores literais, caminhos de arquivo

---

## Checklist de Qualidade

Antes de gerar o manual, verificar:

- [ ] Metadata completa (nome, módulo, datas, classificação)
- [ ] Objetivo claro e conciso
- [ ] Pré-requisitos explícitos
- [ ] Todas as funcionalidades principais cobertas
- [ ] Screenshots existentes e referenciados corretamente
- [ ] Observações numeradas e relevantes
- [ ] Linguagem procedural consistente
- [ ] Rodapé configurado
- [ ] Sumário gerado
- [ ] Numeração de páginas funcionando

---

## Versionamento

### Elaborado vs Revisado
- **Elaborado**: Data da primeira versão
- **Revisado**: Data da última atualização

### Quando incrementar "Revisado"
- Adição de novas funcionalidades
- Correção de erros no manual
- Atualização de screenshots
- Mudanças significativas de fluxo

### Quando criar novo manual
- Mudança de módulo
- Refatoração completa da funcionalidade
- Migração de sistema
