# 📋 Schema JSON - Documentação

## Estrutura Completa

```json
{
  "metadata": {
    "nome_manual": "string (obrigatório)",
    "modulo": "string (obrigatório)",
    "sistema": "string (opcional)",
    "elaborado": "string formato DD/MM/AAAA (obrigatório)",
    "revisado": "string formato DD/MM/AAAA (obrigatório)",
    "classificacao": "string (obrigatório)",
    "logo_path": "string caminho relativo (opcional)"
  },
  "objetivo": "string (obrigatório)",
  "pre_requisito": "string (obrigatório)",
  "funcionalidades": [
    {
      "titulo": "string (obrigatório)",
      "descricao": "string (obrigatório)",
      "prints": ["array de strings (opcional)"],
      "observacoes": ["array de strings (opcional)"],
      "icones": [
        {
          "nome": "string (opcional)",
          "descricao": "string (opcional)"
        }
      ]
    }
  ]
}
```

---

## Campos Detalhados

### 🆕 Novos Recursos (v2.0)

#### Breadcrumbs Automáticos
O gerador automaticamente cria breadcrumbs de navegação em cada funcionalidade usando o padrão: `Módulo >> Nome da Funcionalidade`

**Exemplo renderizado**:
```
Música ao Vivo >> Tela Principal
Música ao Vivo >> Criar Trecho
Música ao Vivo >> Classificar
```

#### Legendas de Imagens
Cada imagem inserida recebe automaticamente uma legenda numerada: `Figura 3.1.1: Nome da Funcionalidade`

#### Ícones com Legendas
Campo novo para documentar ícones utilizados em cada funcionalidade.

---

### metadata (obrigatório)

Informações gerais do manual.

| Campo | Tipo | Obrigatório | Descrição | Exemplo |
|-------|------|-------------|-----------|---------|
| `nome_manual` | string | Sim | Nome completo do manual | "Manual Música ao Vivo - Edição" |
| `modulo` | string | Sim | Nome do módulo/funcionalidade | "Música ao Vivo" |
| `sistema` | string | Não | Nome do sistema maior | "Sistema de Gestão Musical" |
| `elaborado` | string | Sim | Data de criação (DD/MM/AAAA) | "25/01/2026" |
| `revisado` | string | Sim | Data da última revisão | "03/02/2026" |
| `classificacao` | string | Sim | Nível de classificação | "interna", "confidencial", "pública" |
| `logo_path` | string | Não | Caminho relativo para logo | "logo.png" |

---

### objetivo (obrigatório)

**Tipo**: `string`

**Descrição**: Texto que descreve o propósito e objetivo do módulo/funcionalidade documentada.

**Recomendações**:
- 1-3 parágrafos
- Linguagem clara e objetiva
- Descrever o "porquê" da funcionalidade

**Exemplo**:
```json
"objetivo": "Descrever o processo de edição de trechos musicais no sistema, permitindo ao usuário criar, classificar, remover e gerenciar segmentos específicos de áudio dentro das músicas cadastradas."
```

---

### pre_requisito (obrigatório)

**Tipo**: `string`

**Descrição**: Requisitos necessários antes de usar a funcionalidade.

**Deve incluir**:
- Permissões de acesso
- Perfis de usuário necessários
- Configurações prévias
- Dependências de outros módulos

**Exemplo**:
```json
"pre_requisito": "Usuário com perfil de Editor cadastrado no sistema e permissão de acesso ao módulo Música ao Vivo. É necessário que já exista uma música cadastrada no sistema."
```

---

### funcionalidades (obrigatório)

**Tipo**: `array de objetos`

**Descrição**: Lista de funcionalidades detalhadas do módulo.

#### Estrutura de cada funcionalidade:

##### titulo (obrigatório)

**Tipo**: `string`

**Descrição**: Nome da funcionalidade

**Exemplos**:
- "Tela Principal"
- "Criar Trecho"
- "Salvar"
- "Cadastro Pendente"

---

##### descricao (obrigatório)

**Tipo**: `string`

**Descrição**: Texto técnico e procedural explicando como a funcionalidade opera.

**Estilo de escrita**:
- ✅ Linguagem procedural: "Para...", "Ao clicar...", "O sistema..."
- ✅ Passo a passo quando aplicável
- ✅ Referenciar elementos visuais
- ❌ Evitar primeira pessoa
- ❌ Evitar ambiguidade

**Exemplo**:
```json
"descricao": "Para criar um trecho, o usuário deve primeiro clicar no botão 'Criar Trecho' na barra de ferramentas. Em seguida, posicionar o cursor do mouse na posição inicial desejada no wave e, mantendo o botão pressionado, arrastar até a posição final."
```

---

##### prints (opcional)

**Tipo**: `array de strings`

**Descrição**: Lista de nomes de arquivos de screenshot a serem inseridos.

**Recomendações**:
- Caminhos relativos à localização do JSON
- Formatos aceitos: PNG, JPG, JPEG
- Nomes descritivos

**Novo em v2.0**: Cada imagem recebe numeração hierárquica automática com legenda

**Exemplo**:
```json
"prints": [
  "tela_principal.png",
  "criar_trecho_passo1.png",
  "criar_trecho_passo2.png"
]
```

**Renderização no manual**:
```
Figura 3.1.1: Tela Principal
Figura 3.1.2: Tela Principal
Figura 3.1.3: Tela Principal
```

**⚠️ Importante**: 
- Se o arquivo não existir, será exibida mensagem no manual
- As imagens são inseridas centralizadas, com largura de 5.5 polegadas

---

##### observacoes (opcional)

**Tipo**: `array de strings`

**Descrição**: Lista de observações importantes sobre a funcionalidade.

**Quando usar**:
- Alertas críticos
- Restrições
- Comportamentos não óbvios
- Dicas importantes

**Novo em v2.0**: Agora renderizadas com bullets (•) e indentação profissional

**Exemplo**:
```json
"observacoes": [
  "Só após clicar no botão 'Criar Trecho' é que o usuário consegue interagir com o Wave.",
  "A remoção é irreversível após salvar as alterações."
]
```

**Renderização no manual**:
```
Observações:
• Só após clicar no botão 'Criar Trecho'...
• A remoção é irreversível após salvar...
```

---

##### 🆕 icones (opcional - NOVO v2.0)

**Tipo**: `array de objetos`

**Descrição**: Lista de ícones utilizados na funcionalidade com suas descrições.

**Estrutura**:
```json
"icones": [
  {
    "nome": "string",
    "descricao": "string"
  }
]
```

**Quando usar**:
- Explicar ícones de interface
- Descrever símbolos importantes
- Documentar controles visuais

**Exemplo**:
```json
"icones": [
  {
    "nome": "Player",
    "descricao": "Inicia a reprodução do áudio"
  },
  {
    "nome": "Volume",
    "descricao": "Controla o nível de volume"
  },
  {
    "nome": "Velocidade",
    "descricao": "Ajusta a velocidade de reprodução"
  }
]
```

**Renderização no manual**:
```
Ícones Utilizados:
• Player: Inicia a reprodução do áudio
• Volume: Controla o nível de volume
• Velocidade: Ajusta a velocidade de reprodução
```

---

## Exemplo Completo (v2.0)

```json
{
  "metadata": {
    "nome_manual": "Manual Sistema XYZ - Gestão de Usuários",
    "modulo": "Gestão de Usuários",
    "sistema": "Sistema XYZ",
    "elaborado": "01/02/2026",
    "revisado": "03/02/2026",
    "classificacao": "interna",
    "logo_path": "logo_empresa.png"
  },
  "objetivo": "Documentar o processo completo de gestão de usuários do sistema, incluindo cadastro, edição, ativação e desativação de contas.",
  "pre_requisito": "Usuário com perfil de Administrador cadastrado e permissão de acesso ao módulo de Gestão de Usuários.",
  "funcionalidades": [
    {
      "titulo": "Tela de Listagem",
      "descricao": "A tela de listagem exibe todos os usuários cadastrados em formato de tabela. É possível filtrar por nome, email, perfil e status. A barra superior contém os botões 'Novo Usuário' e 'Exportar'.",
      "prints": ["usuarios_listagem.png"],
      "observacoes": [
        "Usuários inativos aparecem em cinza na listagem.",
        "A exportação gera arquivo CSV com todos os filtros aplicados."
      ],
      "icones": [
        {
          "nome": "Novo Usuário",
          "descricao": "Abre formulário para criar novo usuário"
        },
        {
          "nome": "Exportar",
          "descricao": "Exporta dados da listagem em formato CSV"
        },
        {
          "nome": "Filtrar",
          "descricao": "Aplica filtros aos registros exibidos"
        }
      ]
    },
    {
      "titulo": "Criar Usuário",
      "descricao": "Para criar um novo usuário, clicar no botão 'Novo Usuário' na tela de listagem. O sistema exibe um formulário modal com os campos obrigatórios: Nome Completo, Email, Perfil e Senha. Após preencher, clicar em 'Salvar'. O sistema valida o email e, se já existir, exibe mensagem de erro.",
      "prints": ["usuarios_criar_modal.png", "usuarios_criar_validacao.png"],
      "observacoes": [
        "O email deve ser único no sistema.",
        "A senha deve ter no mínimo 8 caracteres, incluindo letras e números.",
        "O perfil determina as permissões do usuário no sistema."
      ],
      "icones": [
        {
          "nome": "Salvar",
          "descricao": "Confirma e salva o novo usuário"
        },
        {
          "nome": "Cancelar",
          "descricao": "Fecha o formulário sem salvar"
        }
      ]
    },
    {
      "titulo": "Editar Usuário",
      "descricao": "Na listagem, clicar no ícone de lápis na linha do usuário desejado. O sistema abre modal com os dados atuais preenchidos. É possível alterar todos os campos exceto o email. Após editar, clicar em 'Salvar' para persistir as alterações.",
      "prints": ["usuarios_editar.png"],
      "observacoes": [
        "O email não pode ser alterado após criação. Para mudar, é necessário criar novo usuário.",
        "Mudanças no perfil afetam as permissões imediatamente."
      ],
      "icones": [
        {
          "nome": "Editar",
          "descricao": "Abre formulário para editar usuário selecionado"
        },
        {
          "nome": "Salvar",
          "descricao": "Confirma as alterações do usuário"
        }
      ]
    }
  ]
}
```

---

## Validação

O sistema valida automaticamente:

✅ Presença de campos obrigatórios  
✅ Formato de datas (DD/MM/AAAA)  
✅ Estrutura de arrays  
✅ Tipos de dados  

❌ Não valida (mas recomenda-se):
- Existência de arquivos de imagem
- Qualidade do conteúdo textual
- Completude das descrições

---

## Ferramentas de Validação

### Online
- [JSONLint](https://jsonlint.com/) - Validação de sintaxe
- [JSON Schema Validator](https://www.jsonschemavalidator.net/)

### Programática

```python
import json

# Validar sintaxe
with open('manual_input.json', 'r') as f:
    dados = json.load(f)

# Validar campos obrigatórios
assert 'metadata' in dados
assert 'objetivo' in dados
assert 'pre_requisito' in dados
assert 'funcionalidades' in dados
```

---

## Dicas de Boas Práticas

### 1. Organização de Arquivos
```
projeto/
├── manual_input.json
├── logo.png
└── screenshots/
    ├── tela1.png
    ├── tela2.png
    └── tela3.png
```

### 2. Nomenclatura de Imagens
```
✅ criar_usuario_modal.png
✅ editar_usuario_form.png
✅ listagem_usuarios.png

❌ img1.png
❌ Screenshot 2024-01-01.png
❌ Captura de Tela.png
```

### 3. Tamanho do JSON
- Funcionalidades: idealmente 4-10 por manual
- Observações: 0-3 por funcionalidade
- Prints: 0-2 por funcionalidade
- Ícones: 0-5 por funcionalidade

### 4. Versionamento
- Manter histórico de JSONs
- Nomear com versão: `manual_v1.json`, `manual_v2.json`
- Documentar mudanças em changelog

### 5. Padrões Profissionais (v2.0+)

#### Breadcrumbs Automáticos
- Gerados automaticamente a partir do módulo e título
- Formato: `Módulo >> Funcionalidade`
- Posicionados antes de cada seção

#### Legendas de Figuras
- Numeração hierárquica: `Figura 3.1.1`, `Figura 3.1.2`, etc.
- Descrevem o conteúdo da imagem
- Posicionadas abaixo de cada figura

#### Estrutura de Observações
- Uso de bullets (•) para melhor legibilidade
- Indentação profissional
- Agrupadas em seção "Observações:"

#### Campo de Ícones
- Documento todos os ícones importantes
- Acompanhados de descrição clara
- Formatados em lista com bullets

---

## Migração para v2.0

Se você possui JSONs na versão anterior, as mudanças são totalmente retrocompatíveis:

- ✅ O campo `icones` é **opcional**
- ✅ Novos recursos automáticos (breadcrumbs, legendas) funcionam sem modificações
- ✅ Estrutura anterior continua funcionando perfeitamente

**Recomendação**: Adicione o campo `icones` aos seus JSONs existentes para aproveitar todos os novos recursos.

---

## Dicas de Boas Práticas

### 1. Organização de Arquivos
```
projeto/
├── manual_input.json
├── logo.png
└── screenshots/
    ├── tela1.png
    ├── tela2.png
    └── tela3.png
```

### 2. Nomenclatura de Imagens
```
✅ criar_usuario_modal.png
✅ editar_usuario_form.png
✅ listagem_usuarios.png

❌ img1.png
❌ Screenshot 2024-01-01.png
❌ Captura de Tela.png
```

### 3. Tamanho do JSON
- Funcionalidades: idealmente 4-10 por manual
- Observações: 0-3 por funcionalidade
- Prints: 0-2 por funcionalidade

### 4. Versionamento
- Manter histórico de JSONs
- Nomear com versão: `manual_v1.json`, `manual_v2.json`
- Documentar mudanças em changelog
