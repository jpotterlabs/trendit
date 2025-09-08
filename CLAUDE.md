# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Backend (FastAPI)
```bash
# Setup and dependencies
cd backend
pip install -r requirements.txt

# Database initialization
python init_db.py

# Development server
uvicorn main:app --reload --port 8000

# Testing
python test_api.py                    # Run all tests
python test_collection_api.py         # Collection tests
python test_query_api.py              # Query tests
python -m pytest                      # pytest-based tests
python -c "import asyncio; from test_api import test_reddit_connection; asyncio.run(test_reddit_connection())"  # Single test
```

### Frontend (Next.js)
```bash
# Setup and development
cd frontend
npm install
npm run dev                          # Development server on port 3000
npm run build                        # Production build
npm start                           # Production server
npm run lint                        # ESLint checking
```

### Full Stack (Docker)
```bash
# Environment setup
cp .env.example .env                 # Configure environment variables

# Docker development
docker-compose up                    # Start all services (backend, frontend, db, redis)
docker-compose up backend           # Start only backend services
docker-compose down                  # Stop all services
```

## Architecture Overview

Trendit is a microservices-based Reddit data collection platform with git submodules architecture:

### Repository Structure
- **backend/**: FastAPI backend (submodule: jpotterlabs/trendit-backend)
- **frontend/**: Next.js frontend (submodule: jpotterlabs/trendit-frontend)  
- **mobile/**: React Native mobile app (submodule: jpotterlabs/trendit-mobile)
- **docs/**: Documentation and deployment guides

### Core Services
- **Authentication**: Auth0 OAuth integration (Google, GitHub) + JWT tokens
- **Data Collection**: Async Reddit API data gathering with PRAW/AsyncPRAW
- **Analytics**: Sentiment analysis and engagement metrics
- **Billing**: Paddle integration with tiered subscriptions
- **Export**: Multi-format data export (CSV, JSON, Parquet)

### Key Backend Components
- **API Endpoints** (`backend/api/`): auth, collect, query, data, export, sentiment, billing, webhooks
- **Services** (`backend/services/`): data_collector, reddit_client, sentiment_analyzer, paddle_service, auth0_service
- **Models** (`backend/models/`): SQLAlchemy database models and connection
- **Database**: PostgreSQL with SQLAlchemy ORM

### Key Frontend Components
- **App Structure** (`frontend/src/app/`): Next.js 15 with App Router
- **Components** (`frontend/src/components/`): analytics, auth, collection, dashboard, export, ui (shadcn/ui)
- **State Management** (`frontend/src/lib/store/`): Zustand stores
- **Authentication** (`frontend/src/lib/contexts/`): Auth0 React provider
- **API Layer** (`frontend/src/lib/api/`): Axios-based API client

## Environment Configuration

### Required Environment Variables
- **Database**: `DATABASE_URL` (PostgreSQL connection string)
- **Reddit API**: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`
- **Auth0**: `AUTH0_DOMAIN`, `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`, `AUTH0_AUDIENCE`
- **Frontend Auth0**: `NEXT_PUBLIC_AUTH0_DOMAIN`, `NEXT_PUBLIC_AUTH0_CLIENT_ID`, `NEXT_PUBLIC_AUTH0_AUDIENCE`
- **Security**: `JWT_SECRET_KEY`, `API_KEY_SALT`
- **Optional**: Paddle billing keys, OpenRouter API key for AI features

### Configuration Files
- `.env` (backend configuration)
- `frontend/.env.local` (frontend configuration)
- Use `.env.example` as template

## Development Patterns

### Backend Code Style
- Follow PEP 8, 88-character line length
- Use type hints and docstrings
- Async/await patterns with proper resource cleanup
- SQLAlchemy ORM with bulk operations for performance
- Pydantic models for request/response validation
- Structured error handling with specific exception types

### Frontend Code Style  
- Next.js 15 App Router patterns
- TypeScript with strict type checking
- Tailwind CSS for styling with shadcn/ui components
- Zustand for state management
- React Hook Form with Zod validation
- Auth0 React for authentication

### Database Schema
- Users table with Auth0 integration fields
- Collection jobs with async status tracking
- Reddit data storage (posts, comments)
- Billing/subscription management
- Usage analytics and rate limiting

## Submodule Management

Each component can be developed and deployed independently:

```bash
# Update submodules to latest
git submodule update --remote

# Work in a submodule
cd backend
git checkout -b feature-branch
# ... make changes ...
git commit -am "changes"
git push

# Update main repo to new submodule commit
cd ..
git add backend
git commit -m "Update backend submodule"
```

## Testing Strategy
- Backend: Direct Python test files with async test patterns
- API testing with httpx for async endpoints
- Database testing with SQLAlchemy fixtures
- Reddit API mocking for collection tests
- Auth0 JWT token validation testing

## Production Deployment
- **Backend**: Docker containers, Vercel serverless, or VPS hosting
- **Frontend**: Vercel (recommended), Netlify, or static hosting
- **Database**: PostgreSQL (AWS RDS, Google Cloud SQL, or self-hosted)
- **Services**: Redis for caching, Auth0 for authentication


 # Using Gemini CLI for Large Codebase Analysis

  When analyzing large codebases or multiple files that might exceed context limits, use the Gemini CLI with its massive
  context window. Use `gemini -p` to leverage Google Gemini's large context capacity.

  ## File and Directory Inclusion Syntax

  Use the `@` syntax to include files and directories in your Gemini prompts. The paths should be relative to WHERE you run the
   gemini command:

  ### Examples:

  **Single file analysis:**
  ```bash
  gemini -p "@src/main.py Explain this file's purpose and structure"

  Multiple files:
  gemini -p "@package.json @src/index.js Analyze the dependencies used in the code"

  Entire directory:
  gemini -p "@src/ Summarize the architecture of this codebase"

  Multiple directories:
  gemini -p "@src/ @tests/ Analyze test coverage for the source code"

  Current directory and subdirectories:
  gemini -p "@./ Give me an overview of this entire project"
  
#
 Or use --all_files flag:
  gemini --all_files -p "Analyze the project structure and dependencies"

  Implementation Verification Examples

  Check if a feature is implemented:
  gemini -p "@src/ @lib/ Has dark mode been implemented in this codebase? Show me the relevant files and functions"

  Verify authentication implementation:
  gemini -p "@src/ @middleware/ Is JWT authentication implemented? List all auth-related endpoints and middleware"

  Check for specific patterns:
  gemini -p "@src/ Are there any React hooks that handle WebSocket connections? List them with file paths"

  Verify error handling:
  gemini -p "@src/ @api/ Is proper error handling implemented for all API endpoints? Show examples of try-catch blocks"

  Check for rate limiting:
  gemini -p "@backend/ @middleware/ Is rate limiting implemented for the API? Show the implementation details"

  Verify caching strategy:
  gemini -p "@src/ @lib/ @services/ Is Redis caching implemented? List all cache-related functions and their usage"

  Check for specific security measures:
  gemini -p "@src/ @api/ Are SQL injection protections implemented? Show how user inputs are sanitized"

  Verify test coverage for features:
  gemini -p "@src/payment/ @tests/ Is the payment processing module fully tested? List all test cases"

  When to Use Gemini CLI

  Use gemini -p when:
  - Analyzing entire codebases or large directories
  - Comparing multiple large files
  - Need to understand project-wide patterns or architecture
  - Current context window is insufficient for the task
  - Working with files totaling more than 100KB
  - Verifying if specific features, patterns, or security measures are implemented
  - Checking for the presence of certain coding patterns across the entire codebase

  Important Notes

  - Paths in @ syntax are relative to your current working directory when invoking gemini
  - The CLI will include file contents directly in the context
  - No need for --yolo flag for read-only analysis
  - Gemini's context window can handle entire codebases that would overflow Claude's context
  - When checking implementations, be specific about what you're looking for to get accurate results # Using Gemini CLI for Large Codebase Analysis


  When analyzing large codebases or multiple files that might exceed context limits, use the Gemini CLI with its massive
  context window. Use `gemini -p` to leverage Google Gemini's large context capacity.


  ## File and Directory Inclusion Syntax


  Use the `@` syntax to include files and directories in your Gemini prompts. The paths should be relative to WHERE you run the
   gemini command:


  ### Examples:


  **Single file analysis:**
  ```bash
  gemini -p "@src/main.py Explain this file's purpose and structure"


  Multiple files:
  gemini -p "@package.json @src/index.js Analyze the dependencies used in the code"


  Entire directory:
  gemini -p "@src/ Summarize the architecture of this codebase"


  Multiple directories:
  gemini -p "@src/ @tests/ Analyze test coverage for the source code"


  Current directory and subdirectories:
  gemini -p "@./ Give me an overview of this entire project"
  # Or use --all_files flag:
  gemini --all_files -p "Analyze the project structure and dependencies"


  Implementation Verification Examples


  Check if a feature is implemented:
  gemini -p "@src/ @lib/ Has dark mode been implemented in this codebase? Show me the relevant files and functions"


  Verify authentication implementation:
  gemini -p "@src/ @middleware/ Is JWT authentication implemented? List all auth-related endpoints and middleware"


  Check for specific patterns:
  gemini -p "@src/ Are there any React hooks that handle WebSocket connections? List them with file paths"


  Verify error handling:
  gemini -p "@src/ @api/ Is proper error handling implemented for all API endpoints? Show examples of try-catch blocks"


  Check for rate limiting:
  gemini -p "@backend/ @middleware/ Is rate limiting implemented for the API? Show the implementation details"


  Verify caching strategy:
  gemini -p "@src/ @lib/ @services/ Is Redis caching implemented? List all cache-related functions and their usage"


  Check for specific security measures:
  gemini -p "@src/ @api/ Are SQL injection protections implemented? Show how user inputs are sanitized"


  Verify test coverage for features:
  gemini -p "@src/payment/ @tests/ Is the payment processing module fully tested? List all test cases"


  When to Use Gemini CLI


  Use gemini -p when:
  - Analyzing entire codebases or large directories
  - Comparing multiple large files
  - Need to understand project-wide patterns or architecture
  - Current context window is insufficient for the task
  - Working with files totaling more than 100KB
  - Verifying if specific features, patterns, or security measures are implemented
  - Checking for the presence of certain coding patterns across the entire codebase


  Important Notes


  - Paths in @ syntax are relative to your current working directory when invoking gemini
  - The CLI will include file contents directly in the context
  - No need for --yolo flag for read-only analysis
  - Gemini's context window can handle entire codebases that would overflow Claude's context
  - When checking implementations, be specific about what you're looking for to get accurate results
