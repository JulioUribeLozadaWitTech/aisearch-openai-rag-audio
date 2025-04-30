import os
import anthropic
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar el cliente de Anthropic
client = anthropic.Client(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def convert_to_mobile(file_path):
    """Convierte un formulario a versión móvil usando Claude"""
    # Leer el contenido del archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Crear el mensaje para Claude
    prompt = f"""
    Necesito adaptar este formulario para que simule la interfaz de un teléfono móvil.
    
    Mi código actual es:
    ```html
    {content}
    ```
    
    Por favor:
    1. Añade los meta tags necesarios para la visualización móvil
    2. Mejora el CSS para una apariencia tipo app móvil (bordes redondeados, sombras, etc.)
    3. Implementa diseño responsive con media queries
    4. Optimiza los campos de entrada para uso táctil (tamaño de botones, espaciado)
    5. Añade animaciones/transiciones suaves típicas de apps móviles
    6. Incluye un mock de "barra de estado" en la parte superior para simular la pantalla del teléfono
    7. Explica brevemente cada cambio importante
    
    El resultado debe ser un archivo HTML autónomo que pueda abrir directamente en un navegador.
    """
    
    # Obtener respuesta de Claude
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    # Extraer el código HTML de la respuesta
    response_text = response.content[0].text
    
    # Intentar extraer el código HTML (asumiendo que está en un bloque de código)
    import re
    html_match = re.search(r'```(?:html)?\s*([\s\S]*?)\s*```', response_text)
    
    if html_match:
        return {
            "html": html_match.group(1),
            "explanation": response_text
        }
    else:
        return {
            "html": "",
            "explanation": response_text
        }

if __name__ == "__main__":
    # Ruta al archivo del formulario (cambia esto por tu ruta)
    form_file = "./app/frontend/index.html"
    
    # Convertir a versión móvil
    result = convert_to_mobile(form_file)
    
    # Guardar el nuevo HTML
    with open("formulario_mobile.html", "w", encoding="utf-8") as f:
        f.write(result["html"])
    
    # Guardar la explicación
    with open("explicacion_cambios.md", "w", encoding="utf-8") as f:
        f.write(result["explanation"])
    
    print("Conversión completada:")
    print("- Formulario móvil guardado en: formulario_mobile.html")
    print("- Explicación guardada en: explicacion_cambios.md")