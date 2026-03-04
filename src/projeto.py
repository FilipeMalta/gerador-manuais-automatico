"""
Módulo utilitário de workspace de projeto.

Centraliza as regras de estrutura de diretórios, persistência de arquivos
enviados pelo usuário (prints, logos) e serialização do manual.json.

Uso típico:
    project_dir = create_project_dir("/tmp/projetos", "meu-manual")
    rel_path    = save_uploaded_file(project_dir, uploaded_file, kind="print")
    json_path   = write_manual_json(project_dir, dados)
    dados       = load_manual_json(project_dir)
"""

import json
from pathlib import Path
from typing import Literal, Protocol, runtime_checkable

MANUAL_JSON_NAME = "manual.json"
ASSETS_SUBDIR = "assets"


@runtime_checkable
class UploadedFileLike(Protocol):
    """Interface mínima compatível com st.UploadedFile e stubs de teste."""
    name: str

    def read(self) -> bytes: ...


def create_project_dir(base_dir: str | Path, project_id: str) -> Path:
    """
    Cria (se necessário) a estrutura de diretórios do projeto e retorna o Path.

    Estrutura criada:
        <base_dir>/<project_id>/
        <base_dir>/<project_id>/assets/

    Args:
        base_dir:   Diretório-raiz onde os projetos são armazenados.
        project_id: Identificador único do projeto (usado como nome de pasta).

    Returns:
        Path do diretório do projeto criado.
    """
    project_dir = Path(base_dir) / project_id
    (project_dir / ASSETS_SUBDIR).mkdir(parents=True, exist_ok=True)
    return project_dir


def save_uploaded_file(
    project_dir: str | Path,
    uploaded_file: UploadedFileLike,
    kind: Literal["print", "logo"] = "print",
) -> str:
    """
    Persiste um arquivo enviado em assets/ e retorna o caminho relativo.

    O caminho retornado é relativo ao project_dir e compatível com o campo
    "prints" e "logo_path" do manual.json (resolvido pelo gerador a partir
    do diretório do JSON).

    Args:
        project_dir:   Diretório do projeto (retornado por create_project_dir).
        uploaded_file: Objeto com .name (str) e .read() -> bytes.
        kind:          "print" ou "logo" — reservado para extensões futuras;
                       atualmente ambos são salvos em assets/.

    Returns:
        Caminho relativo do arquivo salvo, ex.: "assets/screenshot.png".
    """
    assets_dir = Path(project_dir) / ASSETS_SUBDIR
    assets_dir.mkdir(parents=True, exist_ok=True)

    dest = assets_dir / uploaded_file.name
    dest.write_bytes(uploaded_file.read())

    return f"{ASSETS_SUBDIR}/{uploaded_file.name}"


def write_manual_json(project_dir: str | Path, dados: dict) -> Path:
    """
    Serializa o dicionário de dados em manual.json dentro do project_dir.

    Args:
        project_dir: Diretório do projeto.
        dados:       Dicionário com a estrutura completa do manual.

    Returns:
        Path absoluto do arquivo manual.json gravado.
    """
    path = Path(project_dir) / MANUAL_JSON_NAME
    path.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_manual_json(project_dir: str | Path) -> dict:
    """
    Lê e desserializa o manual.json do project_dir.

    Args:
        project_dir: Diretório do projeto.

    Returns:
        Dicionário com o conteúdo do manual.json.

    Raises:
        FileNotFoundError: Se manual.json não existir.
        json.JSONDecodeError: Se o arquivo não for JSON válido.
    """
    path = Path(project_dir) / MANUAL_JSON_NAME
    return json.loads(path.read_text(encoding="utf-8"))
