import json

from groq import Groq
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.crud_category import get_categories
from app.crud.crud_place import get_places
from app.crud.crud_search_history import log_search
from app.models.place import PlaceStatus

client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """
Eres el asistente de recomendación de una app de turismo y recreación en Arequipa, Perú.
Ayudas al usuario a encontrar lugares (piscinas, termales, miradores, lugares campestres, etc.)
usando la herramienta "buscar_lugares" cuando el usuario describa lo que busca.

Reglas:
- NUNCA inventes lugares, precios o datos que no vengan de la herramienta.
- Si te falta información clave (presupuesto, tipo de lugar), puedes preguntar brevemente.
- Responde en español, tono cercano y breve.
- Si la herramienta no devuelve resultados, dilo honestamente y sugiere ampliar la búsqueda.
"""

# Definición de la herramienta que el modelo puede invocar
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "buscar_lugares",
            "description": (
                "Busca lugares turísticos o recreativos en la base de datos según "
                "categoría, precio máximo o texto libre. Úsala cuando el usuario "
                "describa qué tipo de lugar quiere visitar."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "categoria": {
                        "type": "string",
                        "description": "Ej: 'Piscinas', 'Termales', 'Miradores', 'Campestre'. Deja vacío si no aplica.",
                    },
                    "precio_maximo": {
                        "type": "string",
                        "description": "Presupuesto máximo por persona en soles, como número. Ej: '50'. Deja vacío si no aplica.",
                    },
                    "busqueda_libre": {
                        "type": "string",
                        "description": "Palabra clave para buscar en el nombre del lugar. Deja vacío si no aplica.",
                    },
                },
                "required": [],
            },
        },
    }
]


def _resolve_category_id(db: Session, category_name: str | None) -> int | None:
    if not category_name:
        return None
    categories = get_categories(db)
    for cat in categories:
        if cat.name.lower() == category_name.lower():
            return cat.id
    for cat in categories:
        if category_name.lower() in cat.name.lower():
            return cat.id
    return None


def _execute_tool_call(db: Session, user_id: int, arguments: dict) -> list:
    categoria_raw = (arguments.get("categoria") or "").strip()
    precio_raw = (arguments.get("precio_maximo") or "").strip()
    busqueda_raw = (arguments.get("busqueda_libre") or "").strip()

    category_id = _resolve_category_id(db, categoria_raw or None)

    max_price: float | None = None
    if precio_raw:
        try:
            max_price = float(precio_raw)
        except ValueError:
            max_price = None  # el modelo mandó algo no numérico, lo ignoramos

    search_text = busqueda_raw or None

    log_search(
        db, user_id=user_id, query_text=search_text,
        category_id=category_id, max_price=max_price,
    )

    return get_places(
        db, category_id=category_id, max_price=max_price,
        search=search_text, status=PlaceStatus.APPROVED, limit=5,
    )


def get_chatbot_response(db: Session, user_id: int, user_message: str) -> tuple[str, list]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    # 1ra llamada: el modelo decide si necesita datos reales
    completion = client.chat.completions.create(
        model=settings.CHATBOT_MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0.3,
    )

    response_message = completion.choices[0].message
    tool_calls = response_message.tool_calls

    if not tool_calls:
        return response_message.content, []

    messages.append(response_message)

    all_places: list = []
    for tool_call in tool_calls:
        arguments = json.loads(tool_call.function.arguments)
        places = _execute_tool_call(db, user_id, arguments)
        all_places = places

        places_summary = [
            {
                "id": p.id, "nombre": p.name, "categoria": p.category.name,
                "precio": p.price, "direccion": p.address,
            }
            for p in places
        ]
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(places_summary, ensure_ascii=False),
        })

    # 2da llamada: el modelo redacta la respuesta final con datos reales
    final_completion = client.chat.completions.create(
        model=settings.CHATBOT_MODEL, messages=messages, temperature=0.3,
    )

    return final_completion.choices[0].message.content, all_places