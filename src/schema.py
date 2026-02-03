"""
Schema e validação do JSON de entrada
"""

SCHEMA_MANUAL = {
    "type": "object",
    "required": ["metadata", "objetivo", "pre_requisito", "funcionalidades"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["nome_manual", "modulo", "elaborado", "revisado", "classificacao"],
            "properties": {
                "nome_manual": {"type": "string"},
                "modulo": {"type": "string"},
                "sistema": {"type": "string"},
                "elaborado": {"type": "string", "pattern": r"^\d{2}/\d{2}/\d{4}$"},
                "revisado": {"type": "string", "pattern": r"^\d{2}/\d{2}/\d{4}$"},
                "classificacao": {"type": "string"},
                "logo_path": {"type": "string"}
            }
        },
        "objetivo": {"type": "string"},
        "pre_requisito": {"type": "string"},
        "funcionalidades": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["titulo", "descricao"],
                "properties": {
                    "titulo": {"type": "string"},
                    "descricao": {"type": "string"},
                    "prints": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "observacoes": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        }
    }
}
