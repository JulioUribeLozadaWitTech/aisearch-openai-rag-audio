import os
import anthropic
from dotenv import load_dotenv

# Cargar variables de entorno (guarda tu API_KEY en un archivo .env)
load_dotenv()

# Inicializar el cliente de Anthropic
client = anthropic.Client(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def analyze_file(file_path):
    """Analiza un archivo usando Claude 3.7 Sonnet"""
    # Leer el contenido del archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            content = f.read()
        except UnicodeDecodeError:
            return f"No se pudo leer {file_path} (posiblemente archivo binario)"
    
    # Si el archivo está vacío o es muy grande, manejarlo apropiadamente
    if not content.strip():
        return f"El archivo {file_path} está vacío"
    if len(content) > 100000:
        content = content[:100000] + "\n...(truncado)..."
    
    # Crear el mensaje para Claude
    prompt = f"""
    Por favor analiza y explica este archivo: {os.path.basename(file_path)}
    
    ```
    {content}
    ```
    
    Proporciona:
    1. Un resumen de su propósito principal
    2. Explicación de las funciones/clases principales
    3. Cómo se integra con el resto del proyecto (basado en importaciones y funcionalidad)
    4. Cualquier dependencia externa importante
    """
    
    # Obtener respuesta de Claude
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return response.content[0].text

def analyze_project(project_path, exclude_dirs=None, exclude_extensions=None):
    """Analiza todos los archivos en un proyecto"""
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'venv', 'env', '.venv', '__pycache__', 'node_modules']
    if exclude_extensions is None:
        exclude_extensions = ['.pyc', '.pyo', '.pyd', '.so', '.dll', '.class']
    
    results = {}
    
    for root, dirs, files in os.walk(project_path):
        # Excluir directorios no deseados
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            # Excluir archivos por extensión
            if any(file.endswith(ext) for ext in exclude_extensions):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, project_path)
            
            print(f"Analizando: {rel_path}")
            results[rel_path] = analyze_file(file_path)
    
    return results

if __name__ == "__main__":
    # Ruta al proyecto (cambia esto por tu ruta)
    project_path = "./app/frontend"
    
    # Analizar el proyecto
    analysis = analyze_project(project_path)
    
    # Guardar resultados en un archivo markdown
    with open("analisis_proyecto.md", "w", encoding="utf-8") as f:
        f.write("# Análisis del Proyecto\n\n")
        for file_path, explanation in analysis.items():
            f.write(f"## {file_path}\n\n")
            f.write(explanation)
            f.write("\n\n---\n\n")
    
    print(f"Análisis completado y guardado en analisis_proyecto.md")