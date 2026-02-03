"""
Schema JSON Schema para validação de manuais
Versão: 1.0.0
"""

SCHEMA_MANUAL = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Manual Técnico",
    "description": "Schema para estrutura de manuais técnicos Word",
    "type": "object",
    "required": ["metadata", "objetivo", "pre_requisito", "funcionalidades"],
    "additionalProperties": False,
    "properties": {
        "metadata": {
            "type": "object",
            "title": "Metadados do Manual",
            "required": ["nome_manual", "modulo", "elaborado", "revisado", "classificacao"],
            "additionalProperties": False,
            "properties": {
                "nome_manual": {
                    "type": "string",
                    "title": "Nome do Manual",
                    "description": "Nome completo e descritivo do manual",
                    "minLength": 5,
                    "examples": ["Manual Música ao Vivo - Edição"]
                },
                "modulo": {
                    "type": "string",
                    "title": "Módulo/Funcionalidade",
                    "description": "Nome do módulo ou funcionalidade documentada",
                    "minLength": 3,
                    "examples": ["Música ao Vivo", "Gestão de Usuários"]
                },
                "sistema": {
                    "type": "string",
                    "title": "Sistema",
                    "description": "Nome do sistema maior (opcional)",
                    "examples": ["Sistema de Gestão Musical", "Sistema XYZ"]
                },
                "elaborado": {
                    "type": "string",
                    "title": "Data de Elaboração",
                    "description": "Data de criação do manual em formato DD/MM/AAAA",
                    "pattern": "^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/\\d{4}$",
                    "examples": ["25/01/2026", "03/02/2026"]
                },
                "revisado": {
                    "type": "string",
                    "title": "Data de Revisão",
                    "description": "Data da última revisão em formato DD/MM/AAAA",
                    "pattern": "^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/\\d{4}$",
                    "examples": ["03/02/2026"]
                },
                "classificacao": {
                    "type": "string",
                    "title": "Classificação do Documento",
                    "description": "Nível de confidencialidade ou classificação",
                    "enum": ["interna", "confidencial", "pública", "restrita"],
                    "examples": ["interna"]
                },
                "logo_path": {
                    "type": "string",
                    "title": "Caminho da Logo",
                    "description": "Caminho relativo para arquivo de logo (PNG, JPG, JPEG)",
                    "examples": ["logo.png", "logo_empresa.png"]
                }
            }
        },
        "objetivo": {
            "type": "string",
            "title": "Objetivo",
            "description": "Descrição clara do propósito e objetivo do módulo",
            "minLength": 20,
            "examples": [
                "Descrever o processo de edição de trechos musicais no sistema, permitindo ao usuário criar, classificar, remover e gerenciar segmentos específicos de áudio dentro das músicas cadastradas."
            ]
        },
        "pre_requisito": {
            "type": "string",
            "title": "Pré-requisito",
            "description": "Requisitos necessários antes de usar a funcionalidade (permissões, perfis, acessos)",
            "minLength": 10,
            "examples": [
                "Usuário com perfil de Editor cadastrado no sistema e permissão de acesso ao módulo Música ao Vivo. É necessário que já exista uma música cadastrada no sistema."
            ]
        },
        "funcionalidades": {
            "type": "array",
            "title": "Funcionalidades",
            "description": "Lista de funcionalidades documentadas do módulo",
            "minItems": 1,
            "maxItems": 20,
            "items": {
                "type": "object",
                "title": "Funcionalidade",
                "required": ["titulo", "descricao"],
                "additionalProperties": False,
                "properties": {
                    "titulo": {
                        "type": "string",
                        "title": "Título da Funcionalidade",
                        "description": "Nome da funcionalidade",
                        "minLength": 3,
                        "maxLength": 100,
                        "examples": ["Tela Principal", "Criar Trecho", "Salvar", "Cadastro Pendente"]
                    },
                    "descricao": {
                        "type": "string",
                        "title": "Descrição da Funcionalidade",
                        "description": "Texto técnico e procedural (linguagem: Para..., Ao..., O sistema...)",
                        "minLength": 20,
                        "examples": [
                            "Para criar um trecho, o usuário deve primeiro clicar no botão 'Criar Trecho' na barra de ferramentas. Em seguida, posicionar o cursor do mouse na posição inicial desejada no wave e, mantendo o botão pressionado, arrastar até a posição final."
                        ]
                    },
                    "prints": {
                        "type": "array",
                        "title": "Screenshots",
                        "description": "Lista de nomes de arquivos de imagem (PNG, JPG, JPEG)",
                        "items": {
                            "type": "string",
                            "pattern": "\\.(png|jpg|jpeg)$",
                            "examples": ["tela_principal.png", "criar_trecho.png"]
                        },
                        "maxItems": 5
                    },
                    "observacoes": {
                        "type": "array",
                        "title": "Observações",
                        "description": "Lista de observações numeradas (alertas, restrições, dicas)",
                        "items": {
                            "type": "string",
                            "minLength": 10,
                            "examples": [
                                "Só após clicar no botão 'Criar Trecho' é que o usuário consegue interagir com o Wave.",
                                "A remoção é irreversível após salvar as alterações."
                            ]
                        },
                        "maxItems": 5
                    }
                }
            }
        }
    }
}


# Mensagens de erro personalizadas
MENSAGENS_VALIDACAO = {
    "metadata_obrigatorio": "Campo 'metadata' é obrigatório",
    "objetivo_obrigatorio": "Campo 'objetivo' é obrigatório",
    "pre_requisito_obrigatorio": "Campo 'pre_requisito' é obrigatório",
    "funcionalidades_obrigatorio": "Campo 'funcionalidades' é obrigatório",
    "data_invalida": "Data deve estar no formato DD/MM/AAAA",
    "titulo_obrigatorio": "Cada funcionalidade deve ter um 'titulo'",
    "descricao_obrigatoria": "Cada funcionalidade deve ter uma 'descricao'",
    "funcionalidades_vazia": "Deve haver no mínimo 1 funcionalidade",
}


def validar_schema(dados: dict) -> tuple[bool, list]:
    """
    Valida um dicionário contra o schema de manual.
    
    Args:
        dados: Dicionário a validar
        
    Returns:
        Tupla (válido, erros) onde:
        - válido: bool indicando se passou na validação
        - erros: lista de mensagens de erro (vazia se válido)
    """
    import jsonschema
    
    erros = []
    
    try:
        jsonschema.validate(instance=dados, schema=SCHEMA_MANUAL)
        return True, []
    except jsonschema.ValidationError as e:
        return False, [str(e)]
    except jsonschema.SchemaError as e:
        return False, [f"Erro no schema: {str(e)}"]
    except Exception as e:
        return False, [f"Erro de validação: {str(e)}"]
