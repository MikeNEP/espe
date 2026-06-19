import json
import re
import requests

# 1. Función para simular que somos un navegador y obtener el token nuevo
def obtener_token_fresco():
    url_origen = "https://frika.vivolatamz.org/dsports/" # Poné acá la URL de la web que genera el token
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    try:
        response = requests.get(url_origen, headers=headers, timeout=10)
        html = response.text
        
        # Buscamos el patrón del token en el HTML (ejemplo: token=a62119993f...)
        # Esta expresión regular busca lo que esté después de 'token=' hasta las próximas comillas o fin de línea
        match = re.search(r'token=([a-zA-Z0-9\-_]+)', html)
        
        if match:
            return match.group(1)
        else:
            print("No se encontró el token en el HTML. Usando token de respaldo.")
            return "token_temporal_por_error"
    except Exception as e:
        print(f"Error al conectar con la web: {e}")
        return None

# 2. Función principal para actualizar el JSON
def actualizar_json():
    nuevo_token = obtener_token_fresco()
    if not nuevo_token:
        return

    # Hardcodeamos tu IP fija actual o la dejamos dinámica si la web no la valida estricta
    nueva_ip = "190.48.148.232" 

    # Cargar tu mundial.json actual
    with open("mundial.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Recorrer los partidos y actualizar solo los que pertenecen al grupo "Mundial"
    for partido in data:
        if partido["grupo"] == "Mundial":
            url_base = "https://frika.vivolatamz.org/dsports/tracks-v1a1/mono.m3u8"
            partido["url"] = f"{url_base}?ip={nueva_ip}&token={nuevo_token}"
            print(f"Actualizado: {partido['rivales']}")

    # Guardar los cambios de vuelta en el archivo
    with open("mundial.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    actualizar_json()
