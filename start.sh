#!/bin/bash

# Intenta ejecutar Gunicorn
echo "Starting Gunicorn server..."
gunicorn src.main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080

# Si Gunicorn falla, hacer que el contenedor espere indefinidamente
if [ $? -ne 0 ]; then
    echo "Gunicorn failed to start. Entering sleep mode to avoid container shutdown."
    while true; do sleep 3600; done  # Esperar indefinidamente
fi
