# 🐳 Docker Guide for FastAPI Template

This guide explains how to use Docker for both development and production with this FastAPI template.

---

## 🚀 Quick Start

### 1. Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

### 2. Clone and Setup

```bash
git clone <repository-url>
cd Fastapi-Template
cp env.production.example .env.production
# Edit .env.production with your secrets and DB info
```

### 3. Development (Hot Reload)

```bash
docker-compose -f docker-compose.dev.yml up --build
# App: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### 4. Production

```bash
# Set your desired Nginx port in .env.production (default: 80)
NGINX_PORT=800

docker-compose --env-file .env.production --profile production up -d --build
# App: http://localhost:$NGINX_PORT
# Docs: http://localhost:$NGINX_PORT/docs
```

---

## ⚙️ Environment Variables (Production)

| Variable          | Required | Description                                |
| ----------------- | :------: | ------------------------------------------ |
| DATABASE_URL      |   Yes    | SQLAlchemy DB URL for backend and Alembic  |
| POSTGRES_DB       |   Yes    | Postgres DB name (for postgres container)  |
| POSTGRES_USER     |   Yes    | Postgres user (for postgres container)     |
| POSTGRES_PASSWORD |   Yes    | Postgres password (for postgres container) |
| JWT_SECRET_PHRASE |   Yes    | Secret for JWT signing in backend          |
| DEVELOPMENT       |   Yes    | Set to 'false' for production              |
| NGINX_PORT        |   Yes    | External port for Nginx reverse proxy      |

Edit `.env.production` to set these values before running the stack.

---

## 🔄 Changing the Nginx Port

To change the external port Nginx listens on, set `NGINX_PORT` in your `.env.production`:

```env
NGINX_PORT=800
```

This will map the chosen port to Nginx inside the container (which always listens on port 80 internally).

---

## 🛠️ Useful Commands

- **Stop and remove all containers/volumes:**
  ```bash
  docker-compose --env-file .env.production --profile production down --volumes --remove-orphans
  ```
- **Rebuild and restart production:**
  ```bash
  docker-compose --env-file .env.production --profile production up -d --build
  ```
- **View logs:**
  ```bash
  docker-compose --env-file .env.production --profile production logs -f
  ```
- **Check running containers:**
  ```bash
  docker ps
  ```

---

## 🧹 Clean Code & Security

- All secrets and DB credentials are loaded from environment variables.
- No hardcoded secrets or ports (except standard 8000 for backend inside container).
- Only required environment variables are present and documented.

---

## 🤝 Contributing

- Test both development and production flows.
- Update documentation if you add new environment variables or services.
- Keep Docker and Compose files clean and minimal.

---
