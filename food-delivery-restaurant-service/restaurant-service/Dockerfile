# Dockerfile
FROM python:3.10-slim

# Setează directorul de lucru
WORKDIR /app

# Copiază fișierele aplicației
COPY . /app

# Instalează dependențele
RUN pip install --no-cache-dir -r requirements.txt

# Expune portul 5000
EXPOSE 5000

# Define environment variable to specify that Flask is running in development mode
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
