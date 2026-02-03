# 🚀 Guia de Execução

Instruções passo a passo para instalar e executar o gerador de manuais.

---

## 📦 Passo 1: Instalar Dependências

### 1.1 Verificar Python
Certifique-se de ter Python 3.8+ instalado:

```bash
python --version
```

Saída esperada:
```
Python 3.8.0 ou superior
```

### 1.2 Criar Ambiente Virtual (Recomendado)

```bash
# Navegar para a pasta do projeto
cd c:\Users\Aluga.com\gerador-manuais-automatico

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Mac/Linux)
source venv/bin/activate
```

### 1.3 Instalar Dependências

```bash
# Instalar a partir de requirements.txt
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
# Instalar python-docx (geração de Word)
pip install python-docx>=0.8.11

# Instalar Pillow (manipulação de imagens)
pip install Pillow>=10.0.0
```

**Verificar instalação:**

```bash
pip list
```

Você deve ver:
```
python-docx    0.8.11 (ou superior)
Pillow         10.0.0 (ou superior)
```

---

## 🎯 Passo 2: Executar o Gerador

### Usando Linha de Comando

```bash
# Sintaxe geral
python src/gerador_manual.py <input.json> <output.docx>

# Exemplo prático
python src/gerador_manual.py exemplos/input/manual_input.json exemplos/output/Manual.docx
```

### Saída Esperada

```
✅ Manual gerado com sucesso: exemplos/output/Manual.docx
```

---

## 📝 Passo 3: Opções de Execução

### Opção A: Usar Exemplo Fornecido
```bash
python src/gerador_manual.py exemplos/input/manual_input.json exemplos/output/Manual_Musica.docx
```

### Opção B: Seu Próprio JSON
```bash
python src/gerador_manual.py exemplos/input/seu_manual.json exemplos/output/seu_manual.docx
```

### Opção C: Diretórios Diferentes
```bash
python src/gerador_manual.py C:\dados\manual.json C:\output\Manual_Final.docx
```

---

## ✅ Verificar Resultado

1. Abra o arquivo `.docx` gerado
2. Verifique a estrutura:
   - ✅ Capa com logo (se fornecida)
   - ✅ Sumário
   - ✅ Objetivo
   - ✅ Pré-requisito
   - ✅ Funcionalidades com screenshots
   - ✅ Rodapé com numeração de páginas

3. **Atualizar Sumário no Word:**
   - Clique direito no sumário
   - Selecione "Atualizar Campo"
   - Escolha "Atualizar todo o sumário"

---

## ⚠️ Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'docx'"

```
❌ ModuleNotFoundError: No module named 'docx'
```

**Solução:**
```bash
pip install python-docx
```

### Erro: "No such file or directory"

```
❌ FileNotFoundError: [Errno 2] No such file or directory: 'exemplos/input/manual_input.json'
```

**Solução:**
1. Verifique o caminho do arquivo
2. Certifique-se de estar na pasta correta:
   ```bash
   cd c:\Users\Aluga.com\gerador-manuais-automatico
   ```

### Erro: "JSON Decode Error"

```
❌ Erro: JSON inválido em exemplos/input/manual_input.json
```

**Solução:**
1. Valide o JSON online: https://jsonlint.com/
2. Ou via Python:
   ```bash
   python -c "import json; json.load(open('exemplos/input/manual_input.json'))"
   ```

### Aviso: "Imagem não encontrada"

```
⚠️ Erro ao inserir imagem tela_principal.png
[Imagem não encontrada: tela_principal.png]
```

**Solução:**
1. Verifique se a imagem está na pasta do JSON
2. Confirme o nome exato (case-sensitive em Linux/Mac)
3. Certifique-se da extensão (.png, .jpg, .jpeg)

---

## 🔧 Troubleshooting Avançado

### Verificar Permissões
```bash
# Dar permissão de execução (Mac/Linux)
chmod +x src/gerador_manual.py
```

### Desativar Ambiente Virtual
```bash
deactivate
```

### Reinstalar Dependências
```bash
pip uninstall python-docx -y
pip install python-docx --upgrade
```

---

## 📊 Fluxo Completo

```
1. Preparar JSON
   └─> exemplos/input/manual_input.json

2. Adicionar Imagens
   └─> exemplos/input/*.png

3. Instalar Dependências
   └─> pip install -r requirements.txt

4. Executar Gerador
   └─> python src/gerador_manual.py entrada.json saída.docx

5. Verificar Saída
   └─> exemplos/output/saída.docx

6. Abrir em Word
   └─> Atualizar Sumário
   └─> Revisar Conteúdo
   └─> Exportar PDF (opcional)
```

---

## 🎯 Próximas Etapas

Após executar com sucesso:

1. ✅ Revisar manual gerado
2. ✅ Fazer ajustes se necessário
3. ✅ Aplicar branding/estilos corporativos
4. ✅ Distribuir para revisores
5. ✅ Armazenar em repositório de documentos

---

## 💡 Dicas Úteis

### Executar Múltiplos Manuais
```bash
for /R exemplos/input %%f in (*.json) do (
    python src/gerador_manual.py "%%f" "exemplos/output/%%~nf.docx"
)
```

### Criar Script em Lote (batch)
Salve como `gerar.bat`:
```batch
@echo off
cd c:\Users\Aluga.com\gerador-manuais-automatico
python src/gerador_manual.py exemplos/input/manual_input.json exemplos/output/Manual.docx
pause
```

Depois execute:
```bash
gerar.bat
```

### Verificar Versões
```bash
python --version
pip show python-docx
pip show Pillow
```

---

## 📞 Suporte

Consulte a documentação completa:
- [Documentação Técnica](README.md)
- [Padrão Manual](PADRAO_MANUAL.md)
- [Schema JSON](SCHEMA.md)
- [Exemplo Completo](EXEMPLO_USO.md)

