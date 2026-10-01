import logging
import os
import asyncio

from dotenv import load_dotenv
from telegram.ext import Application, ApplicationBuilder

from scraper import buscar_plantilla

# Configuramos el sistema de logs
logging.basicConfig(
    filename="bot.log",  # el nombre del fichero de log
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

# Función que se ejecuta automáticamente al arrancar el bot
async def post_init(app: Application) -> None:
    try:
        await app.bot.send_message(
            chat_id=GROUP_ID,
            text="Hola grupo, soy el mensajero."
        )
        logger.info("Mensaje de bienvenida enviado al grupo.")
    except Exception as e:
        logger.error(f"Error al enviar mensaje al grupo: {e}")

# Función principal
def main() -> None:

    # Crea la app del bot conectándose a Telegram
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    logger.info("Iniciando el bot...")
    # Activa el bot
    app.run_polling()


if __name__ == "__main__":
    main()
