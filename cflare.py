import requests
import csv

def verificar_cloudflare(url):
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        # Verificación de Cloudflare
        usa_cloudflare = any([
            'cloudflare' in headers.get('Server', '').lower(),
            'cf-ray' in headers,
            'cf-cache-status' in headers,
            'cf-request-id' in headers
        ])

        resultado = {
            'URL': url,
            'Usa Cloudflare': 'Sí' if usa_cloudflare else 'No'
        }

        # Agrega los headers al resultado
        for k, v in headers.items():
            resultado[k] = v

        return resultado

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error al conectar con {url}: {e}")
        return {
            'URL': url,
            'Usa Cloudflare': 'Error',
            'Error': str(e)
        }

def guardar_en_csv(resultados, nombre_archivo='resultado_headers.csv'):
    if resultados:
        # Obtener todas las claves únicas para usarlas como encabezados del CSV
        keys = set()
        for res in resultados:
            keys.update(res.keys())
        keys = sorted(keys)

        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(resultados)

        print(f"\n✅ Resultados guardados en: {nombre_archivo}")
    else:
        print("⚠️ No hay resultados para guardar.")

# Lista de URLs (puedes agregar más)
urls = [
    "https://www.cloudflare.com",
    "https://www.google.com",
    "https://www.wikipedia.org"
]

# Ejecutar análisis y guardar resultados
resultados = [verificar_cloudflare(url) for url in urls]
guardar_en_csv(resultados)