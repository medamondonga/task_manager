# Utiliser l'image Python officielle
FROM python:3.13-slim

# Définir le répertoire de travail
WORKDIR /task_manager

# Copier les fichiers de requirements d'abord (optimisation du cache Docker)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Exposer le port
EXPOSE 5000

# Commanda pour lancer l'application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

