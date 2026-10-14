FROM python:3.12-slim

# Evita archivos .pyc y fuerza la salida de consola en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos las librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos los scripts de Python
COPY main.py scraper.py ./

# Creamos la carpeta donde se guardarán bot.log y encontrada.flag
RUN mkdir -p /app/data

# Ejecutamos el script
CMD ["python", "main.py"]