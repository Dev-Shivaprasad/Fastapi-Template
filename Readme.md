# ⚡ FastAPI Full-Stack Template

A production-ready FastAPI full-stack boilerplate to kickstart your modern backend projects with a clean architecture. Built with performance and scalability in mind, this template comes with everything you need for rapid development.

**_<mark>Before Getting Started understand the [Project Structure](#📁-project-structure)</mark>_**

## 🚀 Getting Started

### 1. 📥 Clone the repository

```bash
git clone https://github.com/Dev-Shivaprasad/Fastapi-Tamplate.git

cd fastapi-fullstack-template/backend
```

### 2. 🧪 Create VENV and install dependencies

```bash
uv sync
```

### 3. ⚙️ Create .env file and copy all variables

- There is already a file is provided called `example_env.txt` which contains all the necessary variables just replace them.

```bash
# linux
cp example_env.txt .env
# windows
copy example_env.txt .env
```

### 4. 🔄 Run migrations

- All the DataBase table schemas and models are stored in the `models/` folder

```bash
alembic upgrade head
```

> use `alembic revision --autogenerate -m <name_of_the_migration>` to create the migration  
> or  
>  `alembic revision -m <name_of_the_migration>` for empty migration

### 5. 🚀 Run the server

> All the necessary server configuration is done in the `main.py` file  
> docs / Swagger UI is locally hosted on this link `http://localhost:8000/docs`

```python
uv run main.py
```

---

# ✨ Features

- ⚡ FastAPI + Uvicorn — High-performance async API server

- 🔗 SQLModel — ORM by the creator of FastAPI (based on SQLAlchemy)

- 📦 Alembic — Robust and flexible database migrations

- 🔐 JWT Authentication — Secure token-based auth with PyJWT

- 🧂 Password Hashing — Credential hashing via Bcrypt

- 🚀 Orjson — Super-fast JSON parsing for response speed

- 🧩 Modular Architecture — Clean, scalable, and organized codebase

- 🌱 .env Support — Environment-based flexible configuration

- ⏱️ Rate Limiting — Prevent abuse & DoS

- 🐳 Docker — Dockerfile, docker-compose, and Nginx setup

- 🟥 Redis — Caching layer

---

# 📁 Project Structure

FASTAPI-TEMPLATE/  
│  
├── backend/  
│ ├── alembic`              `# Alembic migration files  
│ ├── authentication/`      `# JWT logic, login, password hashing  
│ ├── database/`            `# DB session setup and initialization  
│ │ └─ cachelayer/`         `# redis cache setup and initialization **(optional)**  
│ ├── docker/`              `# Docker Backend files **(optional)**  
│ │ ├─ .dockerignore`       `# Docker build exclusions  
│ │ └─ .Dockerfile`         `# Backend container definition  
│ ├── models/`              `# SQLModel ORM models  
│ ├── ratelimiter/`         `# ratelimiter setup and initialization **(optional)**  
│ ├── routes/`              `# API route handlers  
│ ├── templates/`           `# router tamplate **(optional)**  
│ ├── utils/`               `# Helper functions  
│ ├── .venv/`               `# uv-managed virtual environment  
│ ├── .python-version`      `# Python version pin  
│ ├── alembic.ini`          `# Alembic configuration  
│ ├── example_env.txt`      `# Example .env file  
│ ├── main.py`              `# App entry point  
│ ├── pyproject.toml`       `# uv dependency definition  
│ └── uv.lock`              `# Dependency lock file  
│  
├── frontend/`              `# Optional frontend (React, Vue, etc.)  
│  
├── docker_and_nginix_configurations/ **(optional)**  
│ ├── docker-compose.yml`     `# Main Docker Compose configuration  
│ ├── docker-compose.dev.yml` `# Development Docker Compose  
│ ├── nginx.conf`             `# Nginx reverse proxy config  
│ ├── env.production.example` `# Production environment template  
│ └── DOCKER.md`              `# Docker documentation  
│  
└── README.md`              `# Main documentation

---

## 🐳 Docker Setup (Optional)

For containerized development and deployment, we now provide comprehensive Docker support:

### Quick Start with Docker

**Development Environment:**

```bash
# Start development environment with hot reload
docker-compose -f ./docker_and_nginix_configurations/docker-compose.dev.yml up --build
```

**Production Environment:**

```bash
# Copy production environment template
cp ./docker_and_nginix_configurations/env.production.example docker_and_nginix_configurations/.env.production
# Edit .env.production with your values
# Start production stack
docker-compose --env-file ./docker_and_nginix_configurations/.env.production --profile production up -d
```

### Docker Features

- 🚀 **Multi-stage builds** : for optimized production images
- 🔄 **Hot reload** : for development
- 🗄️ **PostgreSQL** : for production database
- 🔒 **Nginx** : reverse proxy and abstraction
- 📊 **Health checks** : and monitoring
- 🔐 **Security** : best practices

📖 **Full Docker documentation**: See [DOCKER.md](./docker_and_nginx_configurations/DOCKER.md) for detailed setup and usage instructions.

---

### 🧩 Future Enhancements

Here’s what’s planned or coming soon:

- [x] Rate Limiting — Prevent abuse & DoS

- [x] Nginx — secure routing and abstraction

- [x] Docker — Dockerfile & docker-compose setup

- [x] Redis — Caching layer

---

### 💡 Frontend?

- The frontend/ folder is a placeholder — use it with any frontend framework like:
- ⚛️ React / Next.js

- 🔥 Vue / Nuxt

- 🌌 Astro / SvelteKit

You can ~~remove~~ it if not needed.

---

# 🙌 Contributions

Feel free to open issues, suggest improvements, or submit a pull request. Let’s make this great together 😊.
