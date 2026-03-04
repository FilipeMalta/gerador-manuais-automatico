"""
Interface Web para Gerador de Manuais
Streamlit App
"""

import re
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import tempfile
from difflib import SequenceMatcher
from src.gerador_manual import criar_manual
from src.correcao_ortografica import CorretorOrtografico
from src.config import get_ollama_config
from src.logger import get_logger, log_informacoes_sistema

# Logger para este módulo
logger = get_logger(__name__)

# Inicializar logs na primeira execução
if 'logs_inicializados' not in st.session_state:
    log_informacoes_sistema()
    st.session_state.logs_inicializados = True


# ==================== FUNÇÕES AUXILIARES ====================

def gerar_diff_visual(texto_original: str, texto_corrigido: str) -> str:
    """
    Gera um diff visual colorido entre dois textos.
    
    Palavras removidas aparecem com fundo vermelho.
    Palavras adicionadas aparecem com fundo verde.
    """
    original_palavras = texto_original.split()
    corrigido_palavras = texto_corrigido.split()
    
    matcher = SequenceMatcher(None, original_palavras, corrigido_palavras)
    resultado = []
    
    for operacao, i1, i2, j1, j2 in matcher.get_opcodes():
        if operacao == "equal":
            resultado.extend(original_palavras[i1:i2])
        elif operacao == "delete":
            for palavra in original_palavras[i1:i2]:
                resultado.append(f'<span class="diff-removed">{palavra}</span>')
        elif operacao == "insert":
            for palavra in corrigido_palavras[j1:j2]:
                resultado.append(f'<span class="diff-added">{palavra}</span>')
        elif operacao == "replace":
            for palavra in original_palavras[i1:i2]:
                resultado.append(f'<span class="diff-removed">{palavra}</span>')
            for palavra in corrigido_palavras[j1:j2]:
                resultado.append(f'<span class="diff-added">{palavra}</span>')
    
    return " ".join(resultado)


def calcular_tempo_estimado(tamanho_texto: int, modelo: str = "mixtral") -> str:
    """
    Calcula tempo estimado de correção baseado no tamanho do texto.
    
    Estimativas (aproximadas):
    - mixtral: 1-2 seg por 100 chars
    - neural-chat: 0.5-1 seg por 100 chars
    - mistral: 0.8-1.5 seg por 100 chars
    """
    tempos = {
        "mixtral": (1, 2),
        "neural-chat": (0.5, 1),
        "mistral": (0.8, 1.5),
        "llama2": (1.5, 3)
    }
    
    min_seg, max_seg = tempos.get(modelo, (1, 2))
    tempo_min = max(1, int(tamanho_texto / 100 * min_seg))
    tempo_max = max(1, int(tamanho_texto / 100 * max_seg))
    
    if tempo_min == tempo_max:
        return f"~{tempo_min}s"
    else:
        return f"{tempo_min}-{tempo_max}s"


# Configuração da página
st.set_page_config(
    page_title="Gerador de Manuais",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        color: #0c5460;
    }
    .diff-removed {
        background-color: #ffcccc;
        color: #cc0000;
        text-decoration: line-through;
        padding: 2px 4px;
        border-radius: 3px;
        margin: 0 2px;
    }
    .diff-added {
        background-color: #ccffcc;
        color: #009900;
        font-weight: bold;
        padding: 2px 4px;
        border-radius: 3px;
        margin: 0 2px;
    }
    .diff-container {
        padding: 1rem;
        border-radius: 0.5rem;
        line-height: 1.8;
    }
    .diff-original {
        background-color: #fff5f5;
        border-left: 4px solid #ff6b6b;
    }
    .diff-corrected {
        background-color: #f1fff5;
        border-left: 4px solid #51cf66;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'funcionalidades' not in st.session_state:
    st.session_state.funcionalidades = []
if 'manual_gerado' not in st.session_state:
    st.session_state.manual_gerado = False
if 'objetivo' not in st.session_state:
    st.session_state.objetivo = ""
if 'pre_requisito' not in st.session_state:
    st.session_state.pre_requisito = ""
if 'nome_manual' not in st.session_state:
    st.session_state.nome_manual = ""
if 'modulo' not in st.session_state:
    st.session_state.modulo = ""
if 'sistema' not in st.session_state:
    st.session_state.sistema = ""
if 'elaborado' not in st.session_state:
    st.session_state.elaborado = ""
if 'revisado' not in st.session_state:
    st.session_state.revisado = ""
if 'classificacao' not in st.session_state:
    st.session_state.classificacao = "interna"

# Header
st.markdown('<div class="main-header">🤖 Gerador Automático de Manuais</div>', unsafe_allow_html=True)

# Inicializar corretor ortográfico
if 'corretor' not in st.session_state:
    st.session_state.corretor = CorretorOrtografico(verbose=False)
    logger.info("Corretor Ortográfico inicializado")
if 'ollama_online' not in st.session_state:
    st.session_state.ollama_online = st.session_state.corretor.verificar_disponibilidade()
    status_str = "Online" if st.session_state.ollama_online else "Offline"
    logger.info(f"Status Ollama: {status_str}")

# Sidebar com instruções
with st.sidebar:
    # Status Ollama
    status_ollama = "🟢 Online" if st.session_state.ollama_online else "🔴 Offline"
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Correção com IA:**")
    with col2:
        st.markdown(status_ollama)
    
    if not st.session_state.ollama_online:
        st.warning(
            "⚠️ Ollama não está disponível\n\n"
            "Execute em outro terminal:\n\n"
            "`ollama serve`",
            icon="⚠️"
        )
    
    st.markdown("---")
    st.markdown("### 📖 Como Usar")
    st.markdown("""
    1. **Preencha os metadados** do manual
    2. **Defina objetivo e pré-requisitos**
    3. **Adicione funcionalidades** com descrições e prints
    4. **Gere o manual** em formato .docx
    
    ---
    
    ### 💡 Dicas
    - Use linguagem procedural
    - Screenshots em PNG/JPG
    - Máximo 10MB por imagem
    
    ---
    
    ### 🔗 Links Úteis
    - [Documentação](https://github.com/FilipeMalta/gerador-manuais-automatico)
    - [Padrão de Manual](https://github.com/FilipeMalta/gerador-manuais-automatico)
    """)

# Tabs principais
tab1, tab2, tab3, tab4 = st.tabs(["📋 Metadados", "🎯 Conteúdo", "⚙️ Funcionalidades", "🚀 Gerar Manual"])

# ==================== TAB 1: METADADOS ====================
with tab1:
    st.markdown('<div class="section-header">📋 Informações do Manual</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_manual = st.text_input(
            "Nome do Manual *",
            placeholder="Ex: Manual Música ao Vivo - Edição",
            help="Nome completo que aparecerá na capa",
            value=st.session_state.nome_manual,
            key="nome_manual_input"
        )
        st.session_state.nome_manual = nome_manual
        
        modulo = st.text_input(
            "Módulo *",
            placeholder="Ex: Música ao Vivo",
            help="Nome do módulo/funcionalidade",
            value=st.session_state.modulo,
            key="modulo_input"
        )
        st.session_state.modulo = modulo
        
        sistema = st.text_input(
            "Sistema",
            placeholder="Ex: Sistema de Gestão Musical",
            help="Nome do sistema maior (opcional)",
            value=st.session_state.sistema,
            key="sistema_input"
        )
        st.session_state.sistema = sistema
    
    with col2:
        hoje = datetime.now().strftime("%d/%m/%Y")
        
        elaborado = st.text_input(
            "Data de Elaboração *",
            value=st.session_state.elaborado or hoje,
            help="Formato: DD/MM/AAAA",
            key="elaborado_input"
        )
        st.session_state.elaborado = elaborado
        
        revisado = st.text_input(
            "Data de Revisão *",
            value=st.session_state.revisado or hoje,
            help="Formato: DD/MM/AAAA",
            key="revisado_input"
        )
        st.session_state.revisado = revisado
        
        classificacao = st.selectbox(
            "Classificação *",
            ["interna", "confidencial", "pública", "restrita"],
            index=["interna", "confidencial", "pública", "restrita"].index(st.session_state.classificacao),
            help="Nível de classificação do documento",
            key="classificacao_input"
        )
        st.session_state.classificacao = classificacao
    
    st.markdown("---")
    
    logo_file = st.file_uploader(
        "📷 Logo da Empresa (Opcional)",
        type=["png", "jpg", "jpeg"],
        help="Logo que aparecerá na capa do manual"
    )
    
    if logo_file:
        st.image(logo_file, width=200, caption="Preview do Logo")

# ==================== TAB 2: CONTEÚDO ====================
with tab2:
    st.markdown('<div class="section-header">🎯 Objetivo e Pré-requisitos</div>', unsafe_allow_html=True)
    
    objetivo = st.text_area(
        "Objetivo do Manual *",
        height=150,
        placeholder="Descrever o processo de...",
        help="Descrição clara do propósito do módulo (1-3 parágrafos)",
        value=st.session_state.objetivo,
        key="objetivo_input"
    )
    st.session_state.objetivo = objetivo
    
    st.markdown("**Exemplo:**")
    st.info("Descrever o processo de edição de trechos musicais no sistema, permitindo ao usuário criar, classificar, remover e gerenciar segmentos específicos de áudio.")
    
    st.markdown("---")
    
    pre_requisito = st.text_area(
        "Pré-requisitos *",
        height=100,
        placeholder="Usuário com perfil de...",
        help="Permissões, acessos ou configurações necessárias",
        value=st.session_state.pre_requisito,
        key="pre_requisito_input"
    )
    st.session_state.pre_requisito = pre_requisito
    
    st.markdown("**Exemplo:**")
    st.info("Usuário com perfil de Editor cadastrado no sistema e permissão de acesso ao módulo Música ao Vivo.")

# ==================== TAB 3: FUNCIONALIDADES ====================
with tab3:
    st.markdown('<div class="section-header">⚙️ Adicionar Funcionalidades</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    💡 <strong>Dica:</strong> Adicione uma funcionalidade por vez. Use linguagem procedural: 
    "Para criar um registro, clicar em...", "O sistema exibe...", etc.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    with st.form("form_funcionalidade", clear_on_submit=True):
        st.markdown("### ➕ Nova Funcionalidade")
        
        func_titulo = st.text_input(
            "Título da Funcionalidade *",
            placeholder="Ex: Criar Trecho",
            help="Nome da funcionalidade"
        )
        
        func_descricao = st.text_area(
            "Descrição *",
            height=200,
            placeholder="Para criar um trecho, o usuário deve...",
            help="Descrição técnica e procedural da funcionalidade"
        )
        
        # ==================== CONFIGURAÇÕES DE CORREÇÃO ====================
        # Armazenar texto corrigido na sessão para permitir desfazer
        chave_sessao = f"descricao_corrigida_{id(st.session_state)}"
        descricao_corrigida_sessao = st.session_state.get(chave_sessao, None)
        
        # Opções de correção ortográfica
        corrigir_auto = False  # Padrão: desabilitado
        modelo_selecionado = "mixtral"  # Padrão
        
        if st.session_state.ollama_online:
            st.markdown("---")
            
            # Expander com configurações avançadas
            with st.expander("⚙️ Configurações de Correção Ortográfica", expanded=False):
                st.markdown("**🤖 Opções de Correção com IA**")
                
                col_check, col_info = st.columns([2, 3])
                
                with col_check:
                    corrigir_auto = st.checkbox(
                        "✨ Corrigir automaticamente",
                        value=False,
                        help="Usa IA para corrigir erros ortográficos"
                    )
                
                with col_info:
                    st.info(
                        "📋 A correção é local (Ollama) e não envia dados para servidores externos.",
                        icon="ℹ️"
                    )
                
                # Select de modelo
                col_modelo, col_tempo = st.columns([2, 2])
                
                with col_modelo:
                    modelo_selecionado = st.selectbox(
                        "🧠 Modelo LLM",
                        ["mixtral", "neural-chat", "mistral", "llama2"],
                        help="Escolha o modelo para melhor qualidade/velocidade"
                    )
                
                with col_tempo:
                    tempo_estimado = calcular_tempo_estimado(
                        len(func_descricao) if func_descricao else 0,
                        modelo_selecionado
                    )
                    st.markdown(f"⏱️ **Tempo estimado:** {tempo_estimado}")
                
                # Descrições dos modelos
                modelos_info = {
                    "mixtral": "⚙️ Padrão - Excelente balanço velocidade/qualidade",
                    "neural-chat": "💬 Otimizado para conversação e compreensão contextual",
                    "mistral": "⚡ Mais rápido - Recomendado para textos grandes",
                    "llama2": "🦙 Modelo base - Mais conservador e robusto"
                }
                st.caption(modelos_info.get(modelo_selecionado, ""))
            
            # Botão para pré-visualizar (fora do expander)
            col_preview, col_info = st.columns([3, 2])
            
            with col_preview:
                if corrigir_auto and func_descricao.strip():
                    if st.button(
                        "🔍 Pré-visualizar Correção",
                        use_container_width=True,
                        key="btn_preview_correcao"
                    ):
                        logger.info(
                            f"Pré-visualização de correção acionada | "
                            f"modelo={modelo_selecionado} | tamanho={len(func_descricao)} chars"
                        )
                        with st.spinner(f"🤖 Analisando com {modelo_selecionado}..."):
                            try:
                                # Usar modelo selecionado
                                corretor_modelo = CorretorOrtografico(
                                    model=modelo_selecionado,
                                    verbose=False
                                )
                                descricao_corrigida = corretor_modelo.corrigir_texto(
                                    func_descricao
                                )
                                st.session_state[chave_sessao] = descricao_corrigida
                                logger.info(
                                    f"Pré-visualização concluída | "
                                    f"modelo={modelo_selecionado} | "
                                    f"alterações={len(func_descricao) != len(descricao_corrigida)}"
                                )
                            except Exception as e:
                                logger.error(f"Erro ao corrigir: {str(e)}")
                                st.error(f"❌ Erro ao corrigir: {str(e)}")
                                st.session_state[chave_sessao] = None
            
            with col_info:
                if descricao_corrigida_sessao and descricao_corrigida_sessao != func_descricao:
                    st.success("✅ Correção disponível", icon="✓")
                elif descricao_corrigida_sessao == func_descricao:
                    st.info("✓ Sem erros", icon="ℹ️")
            
            # Mostrar diff visual se houver correção
            if descricao_corrigida_sessao:
                st.markdown("---")
                
                if descricao_corrigida_sessao != func_descricao:
                    # Mostrar comparação lado-a-lado
                    tab_diff, tab_texto = st.tabs(["📊 Diff Visual", "📝 Texto Completo"])
                    
                    with tab_diff:
                        diff_html = gerar_diff_visual(func_descricao, descricao_corrigida_sessao)
                        st.markdown(
                            f'<div class="diff-container diff-original">{diff_html}</div>',
                            unsafe_allow_html=True
                        )
                        st.caption("🔴 = removido | 🟢 = adicionado")
                    
                    with tab_texto:
                        col_orig, col_corr = st.columns(2)
                        
                        with col_orig:
                            st.markdown("**📝 Original:**")
                            st.code(func_descricao, language="text")
                        
                        with col_corr:
                            st.markdown("**✅ Corrigido:**")
                            st.code(descricao_corrigida_sessao, language="text")
                    
                    # Botões de ação
                    col_aceitar, col_desfazer = st.columns(2)
                    
                    with col_aceitar:
                        if st.button(
                            "✓ Aceitar Correção",
                            use_container_width=True,
                            key="btn_aceitar"
                        ):
                            st.session_state[f"func_descricao_final"] = descricao_corrigida_sessao
                            st.success("✅ Correção aceita!")
                    
                    with col_desfazer:
                        if st.button(
                            "↩️ Desfazer",
                            use_container_width=True,
                            key="btn_desfazer"
                        ):
                            st.session_state[chave_sessao] = None
                            st.info("↩️ Correção removida")
                else:
                    st.info("✓ Nenhum erro ortográfico encontrado!", icon="✓")
            
            st.markdown("---")
        
        # Usar texto corrigido se aceito, senão usar original
        descricao_final = st.session_state.get(f"func_descricao_final", None) or func_descricao
        
        
        func_prints = st.file_uploader(
            "Screenshots (Opcional)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            help="Máximo 10MB por imagem"
        )
        
        # Preview dos prints
        if func_prints:
            cols = st.columns(min(len(func_prints), 3))
            for idx, img in enumerate(func_prints):
                with cols[idx % 3]:
                    st.image(img, caption=img.name, use_column_width=True)
        
        st.markdown("---")
        
        st.markdown("**Observações (Opcional)**")
        st.caption("Adicione alertas, restrições ou comportamentos especiais. Uma por linha.")
        
        func_obs = st.text_area(
            "Observações",
            height=100,
            placeholder="Só após clicar em 'Criar' é que o usuário consegue interagir...\nA remoção é irreversível após salvar...",
            help="Cada linha será uma observação numerada (Obs1, Obs2...)",
            label_visibility="collapsed"
        )
        
        submitted = st.form_submit_button("➕ Adicionar Funcionalidade", use_container_width=True)
        
        if submitted:
            if not func_titulo or not func_descricao:
                st.error("❌ Título e Descrição são obrigatórios!")
                logger.warning("Tentativa de adicionar funcionalidade sem título ou descrição")
            else:
                # Usar texto final (corrigido se aceito, original caso contrário)
                descricao_salvar = descricao_final
                
                # Verificar se houve correção
                foi_corrigido = descricao_salvar != func_descricao
                
                # Processar observações
                observacoes = [obs.strip() for obs in func_obs.split('\n') if obs.strip()]
                
                # Salvar prints temporariamente
                prints_salvos = []
                if func_prints:
                    for img in func_prints:
                        prints_salvos.append({
                            'nome': img.name,
                            'data': img.getvalue()
                        })
                
                # Adicionar à lista
                st.session_state.funcionalidades.append({
                    'titulo': func_titulo,
                    'descricao': descricao_salvar,
                    'prints': prints_salvos,
                    'observacoes': observacoes
                })
                
                # Registrar adição de funcionalidade
                logger.info(
                    f"Funcionalidade adicionada | titulo='{func_titulo}' | "
                    f"descricao_chars={len(descricao_salvar)} | "
                    f"corrigido={foi_corrigido} | modelo={modelo_selecionado if foi_corrigido else 'N/A'} | "
                    f"prints={len(prints_salvos)} | obs={len(observacoes)}"
                )
                
                st.success(f"✅ Funcionalidade '{func_titulo}' adicionada com sucesso!")
                st.rerun()
    
    # Mostrar funcionalidades adicionadas
    if st.session_state.funcionalidades:
        st.markdown("---")
        st.markdown("### 📋 Funcionalidades Adicionadas")
        
        for idx, func in enumerate(st.session_state.funcionalidades):
            with st.expander(f"**{idx + 1}. {func['titulo']}**", expanded=False):
                st.markdown(f"**Descrição:**")
                st.write(func['descricao'])
                
                if func['prints']:
                    st.markdown(f"**Screenshots:** {len(func['prints'])} arquivo(s)")
                    cols = st.columns(min(len(func['prints']), 3))
                    for i, print_data in enumerate(func['prints']):
                        with cols[i % 3]:
                            st.caption(print_data['nome'])
                
                if func['observacoes']:
                    st.markdown(f"**Observações:**")
                    for obs_idx, obs in enumerate(func['observacoes'], 1):
                        st.markdown(f"- Obs{obs_idx}: {obs}")
                
                if st.button(f"🗑️ Remover", key=f"remove_{idx}"):
                    st.session_state.funcionalidades.pop(idx)
                    st.success("Funcionalidade removida!")
                    st.rerun()
    else:
        st.info("👆 Nenhuma funcionalidade adicionada ainda. Use o formulário acima para adicionar.")

# ==================== TAB 4: GERAR MANUAL ====================
with tab4:
    st.markdown('<div class="section-header">🚀 Gerar Manual Word</div>', unsafe_allow_html=True)
    
    # Resumo do manual
    st.markdown("### 📊 Resumo do Manual")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Funcionalidades", len(st.session_state.funcionalidades))
    with col2:
        total_prints = sum(len(f['prints']) for f in st.session_state.funcionalidades)
        st.metric("Screenshots", total_prints)
    with col3:
        total_obs = sum(len(f['observacoes']) for f in st.session_state.funcionalidades)
        st.metric("Observações", total_obs)
    with col4:
        campos_obrigatorios = all([
            st.session_state.nome_manual, 
            st.session_state.modulo, 
            st.session_state.elaborado, 
            st.session_state.revisado, 
            st.session_state.objetivo, 
            st.session_state.pre_requisito
        ])
        st.metric("Status", "✅ Pronto" if campos_obrigatorios else "⚠️ Incompleto")
    
    st.markdown("---")
    
    # Preview do JSON
    with st.expander("👁️ Preview do JSON"):
        json_data = {
            "metadata": {
                "nome_manual": st.session_state.nome_manual or "[não preenchido]",
                "modulo": st.session_state.modulo or "[não preenchido]",
                "sistema": st.session_state.sistema or "",
                "elaborado": st.session_state.elaborado,
                "revisado": st.session_state.revisado,
                "classificacao": st.session_state.classificacao
            },
            "objetivo": st.session_state.objetivo or "[não preenchido]",
            "pre_requisito": st.session_state.pre_requisito or "[não preenchido]",
            "funcionalidades": [
                {
                    "titulo": f['titulo'],
                    "descricao": f['descricao'],
                    "prints": [p['nome'] for p in f['prints']],
                    "observacoes": f['observacoes']
                }
                for f in st.session_state.funcionalidades
            ]
        }
        st.json(json_data)
    
    # Botão de gerar
    st.markdown("---")
    
    if st.button("🚀 Gerar Manual .docx", use_container_width=True, type="primary"):
        # Validações
        if not st.session_state.objetivo or not st.session_state.pre_requisito:
            st.error("❌ Preencha Objetivo e Pré-requisitos em 'Conteúdo'!")
        elif not st.session_state.funcionalidades:
            st.error("❌ Adicione pelo menos uma funcionalidade em 'Funcionalidades'!")
        else:
            with st.spinner("⏳ Gerando manual... Isso pode levar alguns segundos."):
                _rerun_needed = False
                try:
                    # Criar diretório temporário
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_path = Path(temp_dir)
                        
                        # Salvar logo se fornecido
                        if logo_file:
                            logo_path = temp_path / "logo.png"
                            with open(logo_path, "wb") as f:
                                f.write(logo_file.getvalue())
                        
                        # Salvar prints
                        prints_dir = temp_path / "prints"
                        prints_dir.mkdir(exist_ok=True)
                        
                        funcionalidades_processadas = []
                        for func in st.session_state.funcionalidades:
                            prints_nomes = []
                            for print_data in func['prints']:
                                print_path = prints_dir / print_data['nome']
                                with open(print_path, "wb") as f:
                                    f.write(print_data['data'])
                                prints_nomes.append(f"prints/{print_data['nome']}")
                            
                            funcionalidades_processadas.append({
                                'titulo': func['titulo'],
                                'descricao': func['descricao'],
                                'prints': prints_nomes,
                                'observacoes': func['observacoes']
                            })
                        
                        # Criar JSON
                        json_data = {
                            "metadata": {
                                "nome_manual": st.session_state.nome_manual,
                                "modulo": st.session_state.modulo,
                                "sistema": st.session_state.sistema or "",
                                "elaborado": st.session_state.elaborado,
                                "revisado": st.session_state.revisado,
                                "classificacao": st.session_state.classificacao,
                            },
                            "objetivo": st.session_state.objetivo,
                            "pre_requisito": st.session_state.pre_requisito,
                            "funcionalidades": funcionalidades_processadas
                        }
                        
                        if logo_file:
                            json_data["metadata"]["logo_path"] = "logo.png"
                        
                        # Salvar JSON temporário
                        json_path = temp_path / "manual_temp.json"
                        with open(json_path, 'w', encoding='utf-8') as f:
                            json.dump(json_data, f, ensure_ascii=False, indent=2)
                        
                        # ============ VERIFICAÇÃO GRAMATICAL ============
                        st.markdown("### 🔍 Verificação Gramatical")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            verificar_grammar = st.button("✅ Verificar Erros", key="verificar_grammar", use_container_width=True)
                        
                        with col2:
                            corrigir_auto = st.button("🔧 Auto-Corrigir", key="corrigir_auto", use_container_width=True)
                        
                        if verificar_grammar:
                            corretor = CorretorGramatical()
                            dados_corrigidos, relatorio = corrigir_json_manual(json_data, automatico=False)
                            
                            if relatorio['campos_corrigidos']:
                                st.warning(f"⚠️ {len(relatorio['campos_corrigidos'])} campo(s) com possíveis erros:", icon="⚠️")
                                
                                for item in relatorio['campos_corrigidos']:
                                    campo_nome = item.get('campo') or item.get('funcionalidade', 'N/A')
                                    num_erros = len(item.get('mudancas', [])) if 'mudancas' in item else item.get('erros', 0)
                                    
                                    with st.expander(f"📝 {campo_nome} ({num_erros} erro(s))"):
                                        if 'detalhes' in item:
                                            for erro in item['detalhes']:
                                                st.write(f"- **{erro['original']}**: {erro['mensagem']}")
                                                if 'sugestoes' in erro and erro['sugestoes']:
                                                    st.write(f"  💡 Sugestões: {', '.join(erro['sugestoes'][:3])}")
                                        elif 'mudancas' in item:
                                            for mudanca in item['mudancas']:
                                                st.write(f"- {mudanca['campo']}")
                            else:
                                st.success("✅ Nenhum erro gramatical detectado!")
                        
                        if corrigir_auto:
                            corretor = CorretorGramatical()
                            dados_corrigidos, relatorio = corrigir_json_manual(json_data, automatico=True)
                            
                            # Atualizar JSON com correções
                            with open(json_path, 'w', encoding='utf-8') as f:
                                json.dump(dados_corrigidos, f, ensure_ascii=False, indent=2)
                            
                            if relatorio['campos_corrigidos']:
                                st.success(f"✅ {len(relatorio['campos_corrigidos'])} campo(s) corrigido(s) automaticamente!")
                            else:
                                st.info("ℹ️ Nenhuma correção necessária")
                        
                        st.markdown("---")
                        
                        # ============ GERAR MANUAL ============
                        # Gerar manual
                        modulo_seguro = re.sub(r'[<>:"/\\|?*]', '-', st.session_state.modulo).replace(' ', '_')
                        output_path = temp_path / f"Manual_{modulo_seguro}.docx"
                        
                        logger.info(
                            f"Iniciando geração de manual | "
                            f"nome='{st.session_state.nome_manual}' | "
                            f"modulo='{st.session_state.modulo}' | "
                            f"funcionalidades={len(st.session_state.funcionalidades)}"
                        )
                        
                        criar_manual(str(json_path), str(output_path))
                        
                        # Ler arquivo gerado
                        with open(output_path, 'rb') as f:
                            docx_bytes = f.read()
                        
                        st.session_state.manual_gerado = True
                        st.session_state.docx_data = docx_bytes
                        st.session_state.manual_nome = f"Manual_{modulo_seguro}.docx"
                        
                        # Log de sucesso
                        logger.info(
                            f"Manual gerado com sucesso | "
                            f"tamanho={len(docx_bytes)} bytes | "
                            f"arquivo='{st.session_state.manual_nome}'"
                        )
                        
                        _rerun_needed = True

                except Exception as e:
                    logger.error(f"Erro ao gerar manual: {str(e)}")
                    st.error(f"❌ Erro ao gerar manual: {str(e)}")

                if _rerun_needed:
                    st.rerun()
    
    # Download do manual gerado
    if st.session_state.manual_gerado:
        st.markdown("---")
        st.markdown("""
        <div class="success-box">
        ✅ <strong>Manual gerado com sucesso!</strong><br>
        Clique no botão abaixo para fazer o download.
        </div>
        """, unsafe_allow_html=True)
        
        st.download_button(
            label="📥 Download Manual .docx",
            data=st.session_state.docx_data,
            file_name=st.session_state.manual_nome,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        
        if st.button("🔄 Gerar Novo Manual", use_container_width=True):
            st.session_state.funcionalidades = []
            st.session_state.manual_gerado = False
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem 0;">
    <p>🤖 <strong>Gerador Automático de Manuais v1.0</strong></p>
    <p>Desenvolvido por um QA</p>
    <p><a href="https://github.com/FilipeMalta/gerador-manuais-automatico" target="_blank">GitHub</a></p>
</div>
""", unsafe_allow_html=True)
