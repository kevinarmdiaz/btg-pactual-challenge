# Primera etapa - Builder
FROM python:3.11.3-slim as builder

# Variables de entorno para Poetry
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION="1.4.2"
ENV POETRY_VIRTUALENVS_IN_PROJECT=1

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Agregar Poetry al PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Crear directorio de trabajo
WORKDIR /code

# Copiar archivos de dependencias de Poetry
COPY pyproject.toml poetry.lock* /code/

# Instalar dependencias del proyecto (sin incluir dependencias de desarrollo)
RUN poetry install --no-ansi --no-interaction --without dev

# Segunda etapa - Imagen final
FROM python:3.11.3-slim

# Directorio de trabajo
WORKDIR /code

# Copiar el entorno virtual desde la etapa builder
COPY --from=builder /code/.venv /code/.venv

# Configurar el PATH para usar el entorno virtual
ENV PATH="/code/.venv/bin:$PATH"

# Copiar el código fuente
COPY ./src /code/src

# Establecer variable para no hacer buffering en Python
ENV PYTHONUNBUFFERED=1

# Ejecutar la aplicación con Gunicorn y Uvicorn
CMD ["gunicorn", "src.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
