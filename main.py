import logging
import os
import time
import requests
from dotenv import load_dotenv

from scraper import buscar_plantilla

# Usamos rutas absolutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Creamos la subcarpeta 'data' para que persista en el volumen de Docker
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

FLAG_FILE = os.path.join(DATA_DIR, "encontrada.flag")
LOG_FILE = os.path.join(DATA_DIR, "bot.log")

# Configuramos el sistema de logs
logging.basicConfig(
    filename=LOG_FILE,  # el nombre del fichero de log
    filemode="a",  # para añadir al final del fichero
    level=logging.INFO,  # El nivel mínimo de alerta que guarda
    format="%(asctime)s - %(levelname)s - %(message)s",  # Devuelve fecha, nivel de alerta y mensaje de alerta
    datefmt="%Y-%m-%d %H:%M:%S",  # Devuelve la fecha de año a segundo
)

# Ponemos en warning la libreria httpx  para que no se llene el log de las peticiones HTTP
logging.getLogger("httpx").setLevel(logging.WARNING)

# El logger general
logger = logging.getLogger(__name__)


# Cargamos el contenido del .env
load_dotenv()

# Asignamos el token y el id a una variable
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GROUP_ID = os.environ["TELEGRAM_GROUP_ID"]

# Funcion para mandar a telegram el mensaje
def enviar_telegram(mensaje: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": GROUP_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()

def main():
    # 1. Si ya hemos avisado antes, salimos sin hacer nada
    if os.path.exists(FLAG_FILE):
        return True

    try:
        resultado = buscar_plantilla()
        if resultado:
            texto, enlace = resultado
            mensaje = f"🚨 <b>Tenemos la plantilla definitiva!</b>\n\n📄 {texto}\n🔗 <a href='{enlace}'>Descargar documento</a>"
            
            enviar_telegram(mensaje)
            logger.info(f"Plantilla encontrada y enviada: {texto}")
            
            # Creamos el archivo flag para no volver a mandarlo cada hora siguiente
            with open(FLAG_FILE, "w") as f:
                f.write("OK")
            return True
        else:
            logger.info("Comprobado: Aún sin plantilla definitiva.")
            return False
            
    except Exception as e:
        logger.error(f"Fallo en la comprobación: {e}")
        return False

if __name__ == "__main__":
    # Bucle con sleep
    while True:
        terminado = main()
        if terminado:
            logger.info("Proceso finalizado. Deteniendo el bot.")
            break  # Sale del bucle si ya encontró la plantilla
        
        time.sleep(3600)  # Espera 1 hora antes de volver a mirar