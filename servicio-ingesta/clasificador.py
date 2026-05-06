import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise EnvironmentError("La variable de entorno GEMINI_API_KEY no está definida.")

genai.configure(api_key=GEMINI_API_KEY)

CATEGORIAS_VALIDAS = {"mercados", "seguros", "macro", "cripto", "otro"}

PROMPT_TEMPLATE = (
    "Eres un clasificador de titulares de noticias financieras. "
    "Clasifica el siguiente titular en exactamente una de estas categorías: "
    "mercados, seguros, macro, cripto, otro. "
    "Responde SOLO con una palabra de esa lista, sin puntuación ni explicación.\n\n"
    "Titular: {titulo}"
)


def clasificar(titulo: str) -> str:
    """Clasifica un titular de noticia financiera usando la API de Gemini."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = PROMPT_TEMPLATE.format(titulo=titulo)

    response = model.generate_content(prompt)
    categoria = response.text.strip().lower()

    if categoria not in CATEGORIAS_VALIDAS:
        categoria = "otro"

    return categoria
