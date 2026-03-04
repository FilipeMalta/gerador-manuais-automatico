"""
Exportação e importação de projeto como .zip autocontido.

Exportação:
  O zip gerado inclui manual.json + assets/ + arquivos avulsos na raiz.
  Pode ser descompactado e passado diretamente ao gerador:
    criar_manual("projeto/manual.json", "Manual.docx")

Importação:
  import_project_zip(zip_bytes, dest_dir) extrai com segurança, valida
  que manual.json existe e tem schema mínimo, retornando o project_dir.

Validação pós-importação:
  find_missing_assets(project_dir) retorna prints referenciados no
  manual.json que não existem em disco.
"""

import io
import json
import zipfile
from pathlib import Path

from src.projeto import ASSETS_SUBDIR, MANUAL_JSON_NAME

# Chaves mínimas obrigatórias no manual.json
_REQUIRED_TOP_KEYS = frozenset({"metadata", "funcionalidades"})
_REQUIRED_META_KEYS = frozenset({"nome_manual", "modulo", "elaborado", "revisado", "classificacao"})


def _validate_manual_schema(dados: dict) -> None:
    """Valida o schema mínimo do manual.json.

    Raises:
        ValueError: Se chaves obrigatórias estiverem faltando ou tipos incorretos.
    """
    if not isinstance(dados, dict):
        raise ValueError("manual.json inválido: o conteúdo deve ser um objeto JSON.")
    missing_top = _REQUIRED_TOP_KEYS - set(dados.keys())
    if missing_top:
        raise ValueError(
            f"manual.json inválido: chave(s) obrigatória(s) faltando: {sorted(missing_top)}"
        )

    meta = dados.get("metadata", {})
    if not isinstance(meta, dict):
        raise ValueError("manual.json inválido: 'metadata' deve ser um objeto.")

    missing_meta = _REQUIRED_META_KEYS - set(meta.keys())
    if missing_meta:
        raise ValueError(
            f"manual.json inválido: metadata faltando: {sorted(missing_meta)}"
        )

    funcs = dados.get("funcionalidades")
    if not isinstance(funcs, list):
        raise ValueError("manual.json inválido: 'funcionalidades' deve ser uma lista.")


def export_project_zip(project_dir: str | Path) -> bytes:
    """
    Empacota o project_dir em um arquivo .zip autocontido e retorna os bytes.

    Regras de inclusão (na ordem abaixo, sem duplicatas):
      1. manual.json  — na raiz do zip
      2. assets/**    — subdiretório de imagens, recursivo
      3. arquivos avulsos na raiz do project_dir (ex: logo.png salvo fora de assets/)

    Args:
        project_dir: Diretório do projeto criado por create_project_dir().

    Returns:
        Bytes do arquivo .zip pronto para download.
    """
    project_dir = Path(project_dir)
    included: set[Path] = set()
    buf = io.BytesIO()

    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        # 1. manual.json
        manual = project_dir / MANUAL_JSON_NAME
        if manual.exists():
            zf.write(manual, arcname=MANUAL_JSON_NAME)
            included.add(manual.resolve())

        # 2. assets/ (recursivo, caminhos com barra-normal p/ compatibilidade)
        assets = project_dir / ASSETS_SUBDIR
        if assets.exists():
            for f in sorted(assets.rglob("*")):
                if f.is_file():
                    zf.write(f, arcname=f.relative_to(project_dir).as_posix())
                    included.add(f.resolve())

        # 3. arquivos avulsos na raiz (logo.png, etc.)
        for f in sorted(project_dir.iterdir()):
            if f.is_file() and f.resolve() not in included:
                zf.write(f, arcname=f.name)

    return buf.getvalue()


def import_project_zip(zip_bytes: bytes, dest_dir: str | Path) -> Path:
    """
    Extrai um zip de projeto para dest_dir com segurança e retorna o project_dir.

    Valida:
      - Bytes formam um zip válido.
      - manual.json está presente no zip.
      - manual.json é JSON válido com schema mínimo obrigatório.
      - Nenhuma entrada possui path traversal (../../).

    Args:
        zip_bytes: Bytes do .zip (ex: st.UploadedFile.read() ou bytes do export).
        dest_dir:  Diretório de destino para extração. Criado se não existir.

    Returns:
        Path(dest_dir) — o project_dir pronto para uso com load_manual_json().

    Raises:
        ValueError: Se o zip for inválido, manual.json estiver ausente/inválido,
                    ou houver entradas com path traversal.
    """
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_resolved = dest_dir.resolve()

    if not zipfile.is_zipfile(io.BytesIO(zip_bytes)):
        raise ValueError("Arquivo não é um zip válido.")

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        names = zf.namelist()

        # Valida que manual.json existe
        if MANUAL_JSON_NAME not in names:
            raise ValueError(
                f"Zip inválido: '{MANUAL_JSON_NAME}' não encontrado no zip."
            )

        # Valida schema do manual.json (leitura in-memory, sem extração ainda)
        try:
            dados_json = json.loads(zf.read(MANUAL_JSON_NAME).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError(f"manual.json não é um JSON válido: {exc}") from exc
        _validate_manual_schema(dados_json)

        # Verifica path traversal em todas as entradas antes de extrair
        for name in names:
            # Normaliza separadores e remove leading slashes
            safe_name = name.replace("\\", "/").lstrip("/")
            dest_path = (dest_dir / safe_name).resolve()
            if not str(dest_path).startswith(str(dest_resolved)):
                raise ValueError(
                    f"Path traversal detectado na entrada do zip: {name!r}"
                )

        # Extração segura entrada a entrada (preserva nomes normalizados)
        for info in zf.infolist():
            safe_name = info.filename.replace("\\", "/").lstrip("/")
            dest_path = dest_dir / safe_name
            if info.is_dir():
                dest_path.mkdir(parents=True, exist_ok=True)
            else:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                dest_path.write_bytes(zf.read(info.filename))

    return dest_dir


def find_missing_assets(project_dir: str | Path) -> list[str]:
    """
    Retorna prints referenciados no manual.json que não existem em disco.

    Args:
        project_dir: Diretório do projeto com manual.json e assets/.

    Returns:
        Lista de caminhos relativos ausentes (ex: ["assets/img.png"]).
        Lista vazia se tudo estiver presente ou não houver prints.
    """
    project_dir = Path(project_dir)
    json_path = project_dir / MANUAL_JSON_NAME
    if not json_path.exists():
        return []

    dados = json.loads(json_path.read_text(encoding="utf-8"))
    missing = []
    for func in dados.get("funcionalidades", []):
        for print_path in func.get("prints", []):
            if not (project_dir / print_path).exists():
                missing.append(print_path)
    return missing
