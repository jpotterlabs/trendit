# Trendit Project Overview

This document provides a comprehensive overview of the Trendit project, a Reddit data collection and analysis platform. It is intended to be used as a context for interacting with the Gemini AI assistant.

## Project Overview

Trendit is a microservices-based application designed to collect, analyze, and visualize data from Reddit. It consists of a backend API, a web-based frontend, and a mobile application.

*   **Backend:** The backend is built with Python and FastAPI. It handles data collection from the Reddit API, performs sentiment analysis, manages user authentication with Auth0, and handles billing with Paddle. It uses a PostgreSQL database for data storage and Redis for caching and rate limiting.
*   **Frontend:** The frontend is a web application built with Next.js and React. It provides a user interface for interacting with the backend API, visualizing data, and managing user accounts. It uses Auth0 for user authentication.
*   **Mobile:** A mobile application for iOS and Android is also part of the project, built with React Native.

## Building and Running

The project can be run locally using Docker Compose or by running each service individually.

### Docker Compose (Recommended)

The `docker-compose.yml` file orchestrates the backend, frontend, PostgreSQL database, and Redis services.

To run the entire application:

```bash
docker-compose up
```

This will start:

*   **Backend:** Accessible at `http://localhost:8000`
*   **Frontend:** Accessible at `http://localhost:3000`
*   **PostgreSQL:** Accessible at `localhost:5432`
*   **Redis:** Accessible at `localhost:6379`

### Individual Services

#### Backend

To run the backend service individually:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload --port 8000
```

#### Frontend

To run the frontend service individually:

```bash
cd frontend
npm install
npm run dev
```

## Development Conventions

*   **Git Submodules:** The project uses git submodules to manage the `backend`, `frontend`, and `mobile` repositories.
*   **Environment Variables:** Configuration for each service is managed through environment variables. Example `.env` files are provided in each service's directory.
*   **API Documentation:** The backend API is documented using OpenAPI (Swagger) and can be accessed at `http://localhost:8000/docs` when the backend is running.
*   **Linting:** The frontend project uses ESLint for code linting. Run `npm run lint` in the `frontend` directory to check for linting errors.
