

<div align="center">
<h1><a href="https://github.com/IHosseini/Shortify"><b>BTG Pactual Fondo de inversión challenge</b></a></h1>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python">
</a>
<a href="https://github.com/psf/black">
    <img src="https://img.shields.io/static/v1?label=code%20style&message=black&color=black&style=flat" alt="Code Style: black">
</a>
<a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat" alt="pre-commit">
</a>
</div>




## Table of Contents
- [About](#-about)
- [Certification](#-certification)
- [How to Build](#-how-to-build)
- [Documentation](#-documentation)
- [Feedback and Contributions](#-feedback-and-contributions)
- [License](#-license)
- [Contacts](#%EF%B8%8F-contacts)

## About 

El presente README expone, los servicios que utilice, para lograr la prueba de concepto para
la empresa BTG Pactual. Este proyecto es un APIRestFul desarrollada en el
framework de python [**FastAPI**](https://fastapi.tiangolo.com/), la base de datos es MongoDb usando el 
ODM (Object Document Manager) Beanie


## Diagramas y Arquitectura del Proyecto
El Fondo Voluntario de Pensión (FPV) de BTG Pactual es un vehículo de inversión a través del cual 
se pueden obtener óptimos rendimientos de acuerdo con las políticas de inversión previstas, 
cumplir con las metas de ahorro o de pensión obligatoria y obtener beneficios tributarios, 
previo cumplimiento de los requisitos de ley. Por su parte, 
los Fondos de Inversión Colectiva (FIC’s) son opciones de inversión que agrupan un número 
de inversionistas, gestionadas por un equipo experto que, a través de la selección de activos globales 
y locales, estructura fondos con objetivos y plazos definidos con el fin común de tener retornos de capital 
y diversificación del riesgo

Se requiere implementar un sistema que permita a los clientes de BTG realizar las siguientes acciones: 
1. Suscribirse a un nuevo fondo (aperturas).
2. Salirse de un fondo actual (cancelaciones). 
3. Ver el historial de últimas transacciones (aperturas y cancelaciones) 
4. se deberá poder enviar una notificación por email o sms dependiendo de la selección del usuario una vez suscrito a dicho fondo

## 🛢️ ERD
Vamos a crear varias colecciones para la base de datos (No Sql).
**users**, **funds**, **log_transactions_funds**

 ### 🧑🏽‍💼Colección: user
    _id: ObjectId
    name: String
    email: String
    phone: String
    balance: Int64

 ### 📈 Colección: funds
    _id: ObjectId
    name: String
    category: String
    minimum_investment_amount: Int32

 ###  📝📈 Colección: log_transactions_funds
      * _id: ObjectId
      --
      user_id: ObjectId
      fund_id: Int32
      transaction_type: String -> Might be [Apertura, Cancelación]
      message: String
      balance: Int64
      date: IsoDate




## Diagrama de secuencia de un usuario suscribiendose a un fondo



## Tecnologías y características

[](https://github.com/fastapi/full-stack-fastapi-template#technology-stack-and-features)


- ⚡ [**FastAPI**](https://fastapi.tiangolo.com/), Como framework de python para la creación del API
    - 🔍 [Pydantic](https://docs.pydantic.dev/), usado por fast api, para la validación de datos y configuraciones
    - 💾 [MongoDB](https://www.mongodb.com/) as the NoSQL database.
    - 🧢[Beanie](https://beanie-odm.dev/) (ODM) object-document mapper para mongo DB que usa Pydantic . 
- 🌩: [AWS](https://aws.amazon.com/): Nube para desplegar el proyecto
	- 🌪: [AWS Cloudformation](https://docs.aws.amazon.com/es_es/AWSCloudFormation/latest/UserGuide/Welcome.html):  Mantener la infraestructura como código (IaC).
- 🐋 [Docker Compose](https://www.docker.com/) for development and production.
- ✅ Tests with [Pytest](https://pytest.org/).
- 📦 [Ruff](): new linter that replaces black, autoflake, isort, and supports more than 600 lint rules.
- 🏎️💨 [Motor](https://motor.readthedocs.io/en/stable/) Driver asincronico para MongoDB
- 
- 🚢 Instrucciones de despliegue usando docker compose
- 🏭 CI (continuous integration) and CD (continuous deployment) basado en github actions con deploy stack para cloudformation.
- ▶ [MakeFile](): Para la ejecución de comandos comunes

## Instalación y configuración

Uso de la API
Endpoints disponibles:



## Documentación interactiva:
FastAPI incluye automáticamente una documentación interactiva usando Swagger UI. Puedes acceder a ella visitando:

- http://127.0.0.1:8000/docs (Swagger UI)
- http://127.0.0.1:8000/redoc (ReDoc)


# Pruebas y coverage 
Ejecutar pruebas unitarias:
El proyecto incluye pruebas unitarias para validar la funcionalidad. Las pruebas se ejecutan con pytest:

pytest --cov=app


## 🚀 Instalación y Configuración

### Pre-requisitos

- Tener instalado [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/).
- Clonar este repositorio:

```bash
git clone https://github.com/tu-usuario/btg-pactual-challenge.git
cd btg-pactual-challenge
```

```bash
cp .env.example .env
```

Configura las variables de entorno necesarias dentro del archivo .env.


## 🏃‍♂️ Instrucciones para ejecutar en local
Sigue estos pasos para ejecutar el proyecto localmente usando Docker:

1. Construir y levantar los contenedores:
```bash
docker-compose up --build
```
Esto levantará la aplicación junto con MongoDB y cualquier otro servicio necesario.


3. Acceder a la documentación interactiva:
FastAPI genera automáticamente documentación de la API con Swagger y ReDoc. Puedes acceder a la documentación en:

Swagger UI: http://localhost:8080/docs
ReDoc: http://localhost:8080/redoc
4. Detener los contenedores:
Para detener los contenedores, ejecuta:
```bash
docker-compose down
```


## ✉️ Contacto
Para cualquier consulta, no dudes en contactarme:

Correo electrónico: kevindiaz9511@gmail.com



# 🤝 Menciones

https://github.com/parfeniukink/medium_fastapi_layered_2023/tree/main

