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

ENV PATH="/code/.venv/bin:$PATH"

COPY ./src /code/src

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

RUN ls -l /code
EXPOSE 8080
# Copiar el script de health check
COPY ./infra/healthcheck.py /code/healthcheck.py

# Dar permisos de ejecución al script de health check (opcional, si lo necesitas ejecutar directamente)
RUN chmod +x /code/healthcheck.py

ENV PYTHONUNBUFFERED=1

CMD ["/start.sh"]