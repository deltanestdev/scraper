import requests
from bs4 import BeautifulSoup

# Obtenemos la web
url = "https://sede.inap.gob.es/es/procedimientos-y-servicios/seleccion/procesos-selectivos-de-cuerpos-y-escalas-generales/cuerpo-de-tecnicos-auxiliares-de-informatica-de-la-administracion-del-estado-ingreso-libre-convocatoria-2025"

# Modificamos el user-agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
}

# Función del scraper

def buscar_plantilla():

    # Descargamos el HTML pasando como argumento la url, el header y el timeout
    respuesta = requests.get(url, headers=headers, timeout=5)

    if respuesta.status_code == 200:
        # Indicamos que la codificación es UTF-8
        respuesta.encoding = "utf-8"
        web = respuesta.text
        with open("web.html", "w") as f:
            f.write(web)
    else:
        print("Error en la petición")
        print(respuesta.status_code)


    # Parseamos el html y obtenemos el objeto soup
    with open("web.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

        # Las plantillas las publican en la cuarta lista
        # Lo importante esta en el div de clase "inap__richText"
        # Filtrado con el selector CSS
        lista = soup.select_one("div.inap__richText > ul:nth-of-type(4)")

        # Inicializamos la variable encontrado
        encontrado = False

        # Bucle for para buscar
        for li in lista.find_all("li", recursive=False):
            primer_enlace = li.find("a")

            if primer_enlace:
                texto_enlace = primer_enlace.get_text(strip=True)
                href = primer_enlace.get("href", "")

                # Comprobamos si contiene el texto buscado
                if "plantilla definitiva" in texto_enlace.lower():
                    encontrado = True
                    print(f"Tenemos la plantilla definitiva por fin")
                    print(f"Texto: {texto_enlace}")
                    print(f"Enlace: {href}")
