# Willcataco Server

This is the backend server for the Willcataco project, built with [FastAPI](https://fastapi.tiangolo.com/).

## Features

- **FastAPI**: High performance, easy to learn, fast to code, ready for production.
- **Health Check**: Endpoint to verify the service status.
- **Modular Structure**: Organized by modules for better scalability.

## Requirements

- Python 3.10+
- PostgreSQL (optional for now, but configured in settings)

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast package management.

1. **Create and activate a virtual environment:**

   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

4. **Environment Configuration:**

   Create a `.env` file in the root directory based on `.env.example` (or use the provided variables):

   ```dotenv
   DB_NAME=willcataco_db
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=willcataco_user
   DB_PASSWORD=willcataco
   ```

## Running the Application

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

## API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure

```
willcataco-server/
├── app/
│   ├── api/            # Main API router
│   ├── core/           # Core configuration
│   ├── modules/        # Feature modules (e.g., health)
│   └── main.py         # Application entry point
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```
