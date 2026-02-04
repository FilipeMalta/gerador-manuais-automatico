"""
Interface Web para Gerador de Manuais
Streamlit App
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import tempfile
from src.gerador_manual import criar_manual

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
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'funcionalidades' not in st.session_state:
    st.session_state.funcionalidades = []
if 'manual_gerado' not in st.session_state:
    st.session_state.manual_gerado = False

# Header
st.markdown('<div class="main-header">🤖 Gerador Automático de Manuais</div>', unsafe_allow_html=True)

# Sidebar com instruções
with st.sidebar:
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
            help="Nome completo que aparecerá na capa"
        )
        
        modulo = st.text_input(
            "Módulo *",
            placeholder="Ex: Música ao Vivo",
            help="Nome do módulo/funcionalidade"
        )
        
        sistema = st.text_input(
            "Sistema",
            placeholder="Ex: Sistema de Gestão Musical",
            help="Nome do sistema maior (opcional)"
        )
    
    with col2:
        hoje = datetime.now().strftime("%d/%m/%Y")
        
        elaborado = st.text_input(
            "Data de Elaboração *",
            value=hoje,
            help="Formato: DD/MM/AAAA"
        )
        
        revisado = st.text_input(
            "Data de Revisão *",
            value=hoje,
            help="Formato: DD/MM/AAAA"
        )
        
        classificacao = st.selectbox(
            "Classificação *",
            ["interna", "confidencial", "pública", "restrita"],
            help="Nível de classificação do documento"
        )
    
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
        help="Descrição clara do propósito do módulo (1-3 parágrafos)"
    )
    
    st.markdown("**Exemplo:**")
    st.info("Descrever o processo de edição de trechos musicais no sistema, permitindo ao usuário criar, classificar, remover e gerenciar segmentos específicos de áudio.")
    
    st.markdown("---")
    
    pre_requisito = st.text_area(
        "Pré-requisitos *",
        height=100,
        placeholder="Usuário com perfil de...",
        help="Permissões, acessos ou configurações necessárias"
    )
    
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
            else:
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
                    'descricao': func_descricao,
                    'prints': prints_salvos,
                    'observacoes': observacoes
                })
                
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
        campos_obrigatorios = all([nome_manual, modulo, elaborado, revisado, objetivo, pre_requisito])
        st.metric("Status", "✅ Pronto" if campos_obrigatorios else "⚠️ Incompleto")
    
    st.markdown("---")
    
    # Preview do JSON
    with st.expander("👁️ Preview do JSON"):
        json_data = {
            "metadata": {
                "nome_manual": nome_manual or "[não preenchido]",
                "modulo": modulo or "[não preenchido]",
                "sistema": sistema or "",
                "elaborado": elaborado,
                "revisado": revisado,
                "classificacao": classificacao
            },
            "objetivo": objetivo or "[não preenchido]",
            "pre_requisito": pre_requisito or "[não preenchido]",
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
        if not nome_manual or not modulo or not elaborado or not revisado:
            st.error("❌ Preencha todos os campos obrigatórios em 'Metadados'!")
        elif not objetivo or not pre_requisito:
            st.error("❌ Preencha Objetivo e Pré-requisitos em 'Conteúdo'!")
        elif not st.session_state.funcionalidades:
            st.error("❌ Adicione pelo menos uma funcionalidade!")
        else:
            with st.spinner("⏳ Gerando manual... Isso pode levar alguns segundos."):
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
                                "nome_manual": nome_manual,
                                "modulo": modulo,
                                "sistema": sistema or "",
                                "elaborado": elaborado,
                                "revisado": revisado,
                                "classificacao": classificacao,
                            },
                            "objetivo": objetivo,
                            "pre_requisito": pre_requisito,
                            "funcionalidades": funcionalidades_processadas
                        }
                        
                        if logo_file:
                            json_data["metadata"]["logo_path"] = "logo.png"
                        
                        # Salvar JSON temporário
                        json_path = temp_path / "manual_temp.json"
                        with open(json_path, 'w', encoding='utf-8') as f:
                            json.dump(json_data, f, ensure_ascii=False, indent=2)
                        
                        # Gerar manual
                        output_path = temp_path / f"Manual_{modulo.replace(' ', '_')}.docx"
                        criar_manual(str(json_path), str(output_path))
                        
                        # Ler arquivo gerado
                        with open(output_path, 'rb') as f:
                            docx_bytes = f.read()
                        
                        st.session_state.manual_gerado = True
                        st.session_state.docx_data = docx_bytes
                        st.session_state.manual_nome = f"Manual_{modulo.replace(' ', '_')}.docx"
                        
                        st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Erro ao gerar manual: {str(e)}")
    
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
    <p>Desenvolvido com ❤️ usando Streamlit</p>
    <p><a href="https://github.com/FilipeMalta/gerador-manuais-automatico" target="_blank">GitHub</a></p>
</div>
""", unsafe_allow_html=True)
