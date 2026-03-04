"""
Interface Web para Gerador de Manuais
Streamlit App
"""

import re
import tempfile
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from src.gerador_manual import criar_manual
from src.corretor_gramatical import CorretorGramatical, corrigir_json_manual
from src.projeto import create_project_dir, save_uploaded_file, write_manual_json
from src.projeto_zip import export_project_zip, find_missing_assets, import_project_zip
from src.logger import get_logger, log_informacoes_sistema

# Logger para este módulo
logger = get_logger(__name__)

# Inicializar logs na primeira execução
if 'logs_inicializados' not in st.session_state:
    log_informacoes_sistema()
    st.session_state.logs_inicializados = True


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

# ---------------------------------------------------------------------------
# Inicializar session state
# ---------------------------------------------------------------------------
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
if 'project_dir' not in st.session_state:
    st.session_state.project_dir = None
if 'ultimo_autosave' not in st.session_state:
    st.session_state.ultimo_autosave = None
if 'session_carregada' not in st.session_state:
    st.session_state.session_carregada = False

# Diretório fixo e persistente — sobrevive ao reinício do app
_WORKSPACE_BASE = Path.home() / "GeradorManuais" / "workspace"

if st.session_state.project_dir is None:
    _fixed_project = create_project_dir(_WORKSPACE_BASE, "projeto")
    st.session_state.project_dir = str(_fixed_project)

_project_dir = Path(st.session_state.project_dir)


# ---------------------------------------------------------------------------
# Helper: auto-save de rascunho em manual.json
# ---------------------------------------------------------------------------

def _autosave_draft() -> None:
    """Grava o estado atual em manual.json no workspace e registra horário."""
    dados = {
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
        "funcionalidades": [
            {
                "titulo": func["titulo"],
                "descricao": func["descricao"],
                "prints": func["prints"],
                "observacoes": func["observacoes"],
            }
            for func in st.session_state.funcionalidades
        ],
    }
    write_manual_json(_project_dir, dados)
    st.session_state.ultimo_autosave = datetime.now().strftime("%H:%M:%S")


# ---------------------------------------------------------------------------
# Helper: popula session_state a partir de project_dir (usado no import)
# ---------------------------------------------------------------------------

def _popular_session_do_projeto(project_dir: Path) -> None:
    """Lê manual.json do project_dir e popula st.session_state.

    Prints ficam como caminhos relativos (assets/...) — sem carregar bytes.
    """
    from src.projeto import load_manual_json
    dados = load_manual_json(project_dir)
    meta = dados.get("metadata", {})

    # Limpa chaves dos widgets para forçar o uso do parâmetro value= no próximo render
    # (evita conflito "widget value set via Session State API + value= parameter")
    _widget_keys = [
        "nome_manual_input", "modulo_input", "sistema_input",
        "elaborado_input", "revisado_input", "classificacao_input",
        "objetivo_input", "pre_requisito_input",
    ]
    for _k in _widget_keys:
        st.session_state.pop(_k, None)

    st.session_state.nome_manual = meta.get("nome_manual", "")
    st.session_state.modulo = meta.get("modulo", "")
    st.session_state.sistema = meta.get("sistema", "")
    st.session_state.elaborado = meta.get("elaborado", "")
    st.session_state.revisado = meta.get("revisado", "")
    st.session_state.classificacao = meta.get("classificacao", "interna")
    st.session_state.objetivo = dados.get("objetivo", "")
    st.session_state.pre_requisito = dados.get("pre_requisito", "")
    st.session_state.project_dir = str(project_dir)

    funcionalidades = []
    for func in dados.get("funcionalidades", []):
        # Mantém apenas prints cujo arquivo realmente existe no disco
        prints_existentes = [
            p for p in func.get("prints", [])
            if (project_dir / p).exists()
        ]
        funcionalidades.append({
            "titulo": func.get("titulo", ""),
            "descricao": func.get("descricao", ""),
            "prints": prints_existentes,
            "observacoes": func.get("observacoes", []),
        })
    st.session_state.funcionalidades = funcionalidades


# ---------------------------------------------------------------------------
# Auto-restore na primeira execução (workspace persistente)
# ---------------------------------------------------------------------------
if not st.session_state.session_carregada:
    _json_persistido = _project_dir / "manual.json"
    if _json_persistido.exists():
        _popular_session_do_projeto(_project_dir)
    st.session_state.session_carregada = True


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.markdown('<div class="main-header">🤖 Gerador Automático de Manuais</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    # ---- Download Rascunho (sempre visível quando há dados) ----
    _rascunho_disponivel = (
        st.session_state.nome_manual
        or st.session_state.modulo
        or st.session_state.objetivo
        or st.session_state.funcionalidades
    )
    if _rascunho_disponivel:
        st.markdown("### 💾 Salvar Rascunho")
        _zip_rascunho = export_project_zip(_project_dir)
        _nome_rascunho = (
            re.sub(r'[<>:"/\\|?*]', '-', st.session_state.modulo or "rascunho")
            .replace(' ', '_')
        )
        st.download_button(
            label="📥 Download Rascunho (.zip)",
            data=_zip_rascunho,
            file_name=f"rascunho_{_nome_rascunho}.zip",
            mime="application/zip",
            use_container_width=True,
            help="Baixe o rascunho para recuperar o projeto depois de fechar o app.",
        )
        st.markdown("---")

    st.markdown("### 📂 Importar Projeto")
    zip_upload = st.file_uploader(
        "Suba um .zip exportado anteriormente",
        type=["zip"],
        key="zip_uploader",
    )
    if zip_upload is not None:
        if st.button("📂 Importar projeto", use_container_width=True):
            try:
                dest = tempfile.mkdtemp(prefix="gerador_import_")
                imported_dir = import_project_zip(zip_upload.read(), dest)
                _popular_session_do_projeto(imported_dir)
                _project_dir = imported_dir
                missing = find_missing_assets(imported_dir)
                if missing:
                    st.warning(
                        f"⚠️ {len(missing)} imagem(ns) referenciada(s) não encontrada(s) "
                        f"no zip: {', '.join(missing)}"
                    )
                st.success("✅ Projeto importado! Verifique as abas.")
                logger.info(f"Projeto importado de zip | dir={dest}")
                st.rerun()
            except ValueError as e:
                st.error(f"❌ {e}")
            except Exception as e:
                logger.error(f"Erro ao importar zip: {e}")
                st.error(f"❌ Erro ao importar: {e}")

    if st.session_state.ultimo_autosave:
        st.caption(f"💾 Rascunho salvo em: {st.session_state.ultimo_autosave}")

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

        func_prints = st.file_uploader(
            "Screenshots (Opcional)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            help="Máximo 10MB por imagem"
        )

        # Preview dos prints (antes de salvar)
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
                observacoes = [obs.strip() for obs in func_obs.split('\n') if obs.strip()]

                # Persistir prints imediatamente no workspace (assets/)
                prints_paths = []
                if func_prints:
                    for img in func_prints:
                        rel_path = save_uploaded_file(_project_dir, img, kind="print")
                        prints_paths.append(rel_path)

                st.session_state.funcionalidades.append({
                    'titulo': func_titulo,
                    'descricao': func_descricao,
                    'prints': prints_paths,   # lista de "assets/xxx.png"
                    'observacoes': observacoes
                })

                logger.info(
                    f"Funcionalidade adicionada | titulo='{func_titulo}' | "
                    f"descricao_chars={len(func_descricao)} | "
                    f"prints={len(prints_paths)} | obs={len(observacoes)}"
                )

                _autosave_draft()
                st.success(f"✅ Funcionalidade '{func_titulo}' adicionada com sucesso!")
                st.rerun()

    # Mostrar funcionalidades adicionadas
    if st.session_state.funcionalidades:
        st.markdown("---")
        st.markdown("### 📋 Funcionalidades Adicionadas")

        for idx, func in enumerate(st.session_state.funcionalidades):
            with st.expander(f"**{idx + 1}. {func['titulo']}**", expanded=False):
                st.markdown("**Descrição:**")
                st.write(func['descricao'])

                if func['prints']:
                    st.markdown(f"**Screenshots:** {len(func['prints'])} arquivo(s)")
                    cols = st.columns(min(len(func['prints']), 3))
                    for i, rel_path in enumerate(func['prints']):
                        with cols[i % 3]:
                            img_path = _project_dir / rel_path
                            if img_path.exists():
                                st.image(str(img_path), caption=img_path.name)
                            else:
                                st.caption(f"⚠️ {rel_path}")

                if func['observacoes']:
                    st.markdown("**Observações:**")
                    for obs_idx, obs in enumerate(func['observacoes'], 1):
                        st.markdown(f"- Obs{obs_idx}: {obs}")

                if st.button(f"🗑️ Remover", key=f"remove_{idx}"):
                    st.session_state.funcionalidades.pop(idx)
                    _autosave_draft()
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
        json_preview = {
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
                    "prints": f['prints'],   # já são strings "assets/..."
                    "observacoes": f['observacoes']
                }
                for f in st.session_state.funcionalidades
            ]
        }
        st.json(json_preview)

    # Botão de gerar
    st.markdown("---")

    if st.button("🚀 Gerar Manual .docx", use_container_width=True, type="primary"):
        if not st.session_state.objetivo or not st.session_state.pre_requisito:
            st.error("❌ Preencha Objetivo e Pré-requisitos em 'Conteúdo'!")
        elif not st.session_state.funcionalidades:
            st.error("❌ Adicione pelo menos uma funcionalidade em 'Funcionalidades'!")
        else:
            with st.spinner("⏳ Gerando manual... Isso pode levar alguns segundos."):
                _rerun_needed = False
                try:
                    # Salvar logo no workspace (avulso na raiz, fora de assets/)
                    if logo_file:
                        logo_path = _project_dir / "logo.png"
                        logo_path.write_bytes(logo_file.getvalue())

                    # Construir JSON — prints já estão em assets/ no workspace
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
                        "funcionalidades": [
                            {
                                "titulo": func["titulo"],
                                "descricao": func["descricao"],
                                "prints": func["prints"],
                                "observacoes": func["observacoes"],
                            }
                            for func in st.session_state.funcionalidades
                        ],
                    }

                    if logo_file:
                        json_data["metadata"]["logo_path"] = "logo.png"

                    # ============ VERIFICAÇÃO GRAMATICAL ============
                    st.markdown("### 🔍 Verificação Gramatical")

                    col1, col2 = st.columns(2)
                    with col1:
                        verificar_grammar = st.button("✅ Verificar Erros", key="verificar_grammar", use_container_width=True)
                    with col2:
                        corrigir_auto = st.button("🔧 Auto-Corrigir", key="corrigir_auto", use_container_width=True)

                    if verificar_grammar:
                        corretor = CorretorGramatical()
                        _, relatorio = corrigir_json_manual(json_data, automatico=False)
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
                        json_data, relatorio = corrigir_json_manual(json_data, automatico=True)
                        if relatorio['campos_corrigidos']:
                            st.success(f"✅ {len(relatorio['campos_corrigidos'])} campo(s) corrigido(s) automaticamente!")
                        else:
                            st.info("ℹ️ Nenhuma correção necessária")

                    st.markdown("---")

                    # ============ GRAVAR JSON NO WORKSPACE ============
                    json_path = write_manual_json(_project_dir, json_data)

                    # ============ GERAR MANUAL (docx em temp isolado) ============
                    modulo_seguro = re.sub(r'[<>:"/\\|?*]', '-', st.session_state.modulo).replace(' ', '_')

                    with tempfile.TemporaryDirectory() as out_dir:
                        output_path = Path(out_dir) / f"Manual_{modulo_seguro}.docx"

                        logger.info(
                            f"Iniciando geração de manual | "
                            f"nome='{st.session_state.nome_manual}' | "
                            f"modulo='{st.session_state.modulo}' | "
                            f"funcionalidades={len(st.session_state.funcionalidades)}"
                        )

                        criar_manual(str(json_path), str(output_path))
                        docx_bytes = output_path.read_bytes()

                    # Zip do workspace (json + assets + logo)
                    zip_bytes = export_project_zip(_project_dir)

                    st.session_state.manual_gerado = True
                    st.session_state.docx_data = docx_bytes
                    st.session_state.manual_nome = f"Manual_{modulo_seguro}.docx"
                    st.session_state.zip_data = zip_bytes
                    st.session_state.zip_nome = f"Manual_{modulo_seguro}.zip"

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
        Clique nos botões abaixo para fazer o download.
        </div>
        """, unsafe_allow_html=True)

        col_docx, col_zip = st.columns(2)
        with col_docx:
            st.download_button(
                label="📥 Download Manual .docx",
                data=st.session_state.docx_data,
                file_name=st.session_state.manual_nome,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        with col_zip:
            st.download_button(
                label="📦 Exportar projeto (.zip)",
                data=st.session_state.zip_data,
                file_name=st.session_state.zip_nome,
                mime="application/zip",
                use_container_width=True
            )

        if st.button("🔄 Gerar Novo Manual", use_container_width=True):
            st.session_state.funcionalidades = []
            st.session_state.manual_gerado = False
            st.rerun()

# Auto-save silencioso no final de cada render (capta mudanças nos campos de texto)
_any_data = (
    st.session_state.nome_manual
    or st.session_state.modulo
    or st.session_state.objetivo
    or st.session_state.funcionalidades
)
if _any_data:
    _autosave_draft()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem 0;">
    <p>🤖 <strong>Gerador Automático de Manuais v1.0</strong></p>
    <p>Desenvolvido por um QA</p>
    <p><a href="https://github.com/FilipeMalta/gerador-manuais-automatico" target="_blank">GitHub</a></p>
</div>
""", unsafe_allow_html=True)
