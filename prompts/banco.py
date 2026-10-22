
BANCO_DE_PROMPTS = [
    {
        "nombre": "extraer_ingredientes",
        "system_instruction": (
            "Eres un asistente que organiza información de costos "
            "para pequeñas empresas. Extrae del texto el nombre del "
            "producto, los ingredientes, las cantidades, las unidades "
            "y los precios informados. No inventes datos que no estén "
            "en el texto. Si un dato no aparece, utiliza null. "
            "Responde únicamente con un objeto JSON válido."
        ),
        "ejemplo_usuario": (
            "Para preparar galletas uso 500 gramos de harina "
            "que cuestan 800 pesos, 200 gramos de mantequilla "
            "que cuestan 1500 pesos y 150 gramos de azúcar "
            "que cuestan 300 pesos."
        ),
        "claves_esperadas": ["producto", "ingredientes"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "producto": {"type": "STRING"},
                "ingredientes": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "nombre": {"type": "STRING"},
                            "cantidad": {
                                "type": "NUMBER",
                                "nullable": True
                            },
                            "unidad": {
                                "type": "STRING",
                                "nullable": True
                            },
                            "precio_clp": {
                                "type": "NUMBER",
                                "nullable": True
                            }
                        },
                        "required": [
                            "nombre",
                            "cantidad",
                            "unidad",
                            "precio_clp"
                        ]
                    }
                }
            },
            "required": ["producto", "ingredientes"]
        }
    },
    {
        "nombre": "detectar_datos_faltantes",
        "system_instruction": (
            "Analiza la información de una receta para una PYME. "
            "Identifica qué datos faltan entre cantidad, unidad y "
            "precio de cada ingrediente. No inventes información. "
            "Devuelve un objeto JSON con la clave ingredientes, que "
            "contenga el nombre de cada ingrediente y una lista "
            "de sus datos faltantes."
        ),
        "ejemplo_usuario": (
            "Para hacer un queque uso 3 huevos que cuestan 900 pesos, "
            "harina por 700 pesos y 200 gramos de azúcar."
        ),
        "claves_esperadas": ["ingredientes"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "ingredientes": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "nombre": {"type": "STRING"},
                            "datos_faltantes": {
                                "type": "ARRAY",
                                "items": {"type": "STRING"}
                            }
                        },
                        "required": ["nombre", "datos_faltantes"]
                    }
                }
            },
            "required": ["ingredientes"]
        }
    },
    {
        "nombre": "estructurar_receta",
        "system_instruction": (
            "Eres un asistente de organización de costos para PYMEs. "
            "Organiza la información de una receta en un objeto JSON "
            "con el nombre del producto y una lista de ingredientes "
            "con nombre, cantidad, unidad y precio_clp. Usa null "
            "cuando el texto no informe un dato. No calcules precios "
            "ni inventes cantidades. Responde solo con JSON válido."
        ),
        "ejemplo_usuario": (
            "Brownies: 250 gramos de chocolate por 2000 pesos, "
            "100 gramos de mantequilla por 1000 pesos."
        ),
        "claves_esperadas": ["producto", "ingredientes"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "producto": {"type": "STRING"},
                "ingredientes": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "nombre": {"type": "STRING"},
                            "cantidad": {
                                "type": "NUMBER",
                                "nullable": True
                            },
                            "unidad": {
                                "type": "STRING",
                                "nullable": True
                            },
                            "precio_clp": {
                                "type": "NUMBER",
                                "nullable": True
                            }
                        },
                        "required": [
                            "nombre",
                            "cantidad",
                            "unidad",
                            "precio_clp"
                        ]
                    }
                }
            },
            "required": ["producto", "ingredientes"]
        }
    }
]
