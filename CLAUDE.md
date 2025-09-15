# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📋 ESSENTIAL: Complete Development Workflow

**IMPORTANT**: For the complete development ceremony including feature branches, code review integration, and human-AI collaboration protocols, see **[DEVELOPMENT_WORKFLOW.md](./DEVELOPMENT_WORKFLOW.md)**.

This document covers basic setup and commands. The workflow document covers the complete operational procedures for professional development.

## 🚨 CRITICAL: Directory Navigation & Git Workflow

### Directory Structure Understanding
```
trendit/ (ROOT REPO)
├── backend/          → jpotterlabs/trendit-backend (SUBMODULE)
├── frontend/         → jpotterlabs/trendit-frontend (SUBMODULE)  
├── mobile/           → jpotterlabs/trendit-mobile (SUBMODULE)
├── docs/             → Documentation
├── CLAUDE.md         → This file
└── TESTING_STRATEGY.md
```

### Critical Navigation Rules

#### ⚠️ ALWAYS Verify Your Location
```bash
# Before any git operation, ALWAYS check:
pwd                   # Verify current directory
git remote -v         # Verify which repository you're in
```

#### Directory Navigation Commands
```bash
# Navigate to root repo
cd /home/jason/projects/jpotterlabs/trendit

# Navigate to specific submodule
cd /home/jason/projects/jpotterlabs/trendit/backend
cd /home/jason/projects/jpotterlabs/trendit/frontend
cd /home/jason/projects/jpotterlabs/trendit/mobile

# NEVER use relative cd commands across sessions - bash maintains working directory
# ALWAYS use absolute paths when switching between root and submodules
```

### Git Submodule Workflow (CRITICAL)

#### Making Changes in Submodules
```bash
# 1. ALWAYS work in the submodule first
cd /home/jason/projects/jpotterlabs/trendit/backend

# 2. Check submodule status
git status              # Should show branch name, not "HEAD detached"
git branch -a           # View available branches

# 3. If in detached HEAD state, fix it:
git checkout main       # Switch to main branch first
git pull               # Get latest changes

# 4. Create feature branch in submodule
git checkout -b feature/your-feature-name

# 5. Make your changes and commit
git add .
git commit -m "Your commit message"
git push -u origin feature/your-feature-name

# 6. Create PR for submodule (CRITICAL STEP)
gh pr create --title "Your feature title" --body "$(cat <<'EOF'
## Summary
• Brief description of changes
• Impact on the system

## Technical Details
• Key implementation details
• Architecture considerations

## Test Plan
- [ ] Test item 1
- [ ] Test item 2

🤖 Generated with [Claude Code](https://claude.ai/code)
EOF
)"

# 7. REPEAT for additional submodules if needed (e.g., frontend)
cd /home/jason/projects/jpotterlabs/trendit/frontend
git checkout -b feature/your-feature-name
# ... make changes, commit, push, create PR ...

# 8. THEN update root repo
cd /home/jason/projects/jpotterlabs/trendit

# 9. Create feature branch in root repo
git checkout -b feature/your-feature-name

# 10. Stage submodule pointer updates
git add backend frontend    # Stage all changed submodules

# 11. Commit root repo changes
git commit -m "Update submodules: your change description"
git push -u origin feature/your-feature-name

# 12. Create PR for root repository
gh pr create --title "Your feature title" --body "$(cat <<'EOF'
## Summary
Updates submodules to include [feature description]

## Submodule Updates
**Backend Submodule**: PR #XX - [description]
**Frontend Submodule**: PR #XX - [description]

## Merge Order
1. First: Merge backend submodule PR
2. Second: Merge frontend submodule PR
3. Third: Merge this root repository PR

🤖 Generated with [Claude Code](https://claude.ai/code)
EOF
)"
```

#### Pull Request Creation and Merge Order
1. **First**: Create PR for each submodule repository using `gh pr create`
2. **Second**: Create PR for root repository (includes submodule updates) using `gh pr create`
3. **Review**: All PRs include detailed descriptions, test plans, and merge instructions
4. **Merge Order**: Submodule PRs first, then root repo PR
5. **Critical**: ALWAYS use `gh pr create` - pushing branches alone does NOT create PRs

### Common Pitfalls to AVOID

#### ❌ DON'T: Create branches in wrong repository
```bash
# WRONG - creating feature branch in root for submodule changes
cd /home/jason/projects/jpotterlabs/trendit
git checkout -b feature/backend-changes  # ❌ WRONG
# Then editing backend files
```

#### ❌ DON'T: Ignore detached HEAD warnings
```bash
# If you see "HEAD detached at abc123" - FIX IT IMMEDIATELY
git checkout main
git pull
```

#### ❌ DON'T: Use relative navigation
```bash
cd backend    # ❌ Might fail if not in root
cd ../frontend  # ❌ Might fail if bash session is in wrong dir
```

#### ✅ DO: Use absolute paths
```bash
cd /home/jason/projects/jpotterlabs/trendit/backend   # ✅ CORRECT
cd /home/jason/projects/jpotterlabs/trendit/frontend  # ✅ CORRECT
```

### Directory Verification Checklist

Before any git operation:
- [ ] Run `pwd` to confirm location
- [ ] Run `git remote -v` to confirm repository
- [ ] Run `git status` to check branch and state
- [ ] If in submodule, ensure NOT in detached HEAD state

### Emergency Recovery

If you get lost or make mistakes:
```bash
# 1. Find where you are
pwd
git remote -v

# 2. Go to known good state
cd /home/jason/projects/jpotterlabs/trendit
git status

# 3. Reset submodules if needed
git submodule update --init --recursive

# 4. Check all submodule states
cd backend && git status && cd ..
cd frontend && git status && cd ..
cd mobile && git status && cd ..
```

## 🤖 CodeRabbit Review Assessment Process

After creating PRs in the git ceremony workflow, wait for CodeRabbit automated code review completion, then follow this systematic assessment process:

### **Review Assessment Methodology**

**Step 1: Retrieve CodeRabbit Comments**
```bash
# For each PR, review CodeRabbit feedback directly
gh pr view [PR_NUMBER] --repo [REPOSITORY] --comments
```

**Step 2: Categorize Issues by Severity**

Organize CodeRabbit findings into these priority categories:

#### **🚨 Critical Issues (Must Fix Before Merge):**
- **Security vulnerabilities** (missing `rel="noopener"`, XSS risks, etc.)
- **Breaking changes** that affect functionality
- **Production deployment blockers**

#### **⚠️ Should Fix (Highly Recommended):**
- **Code quality issues** (variable shadowing, type errors)
- **Performance problems** (inefficient algorithms, memory leaks)
- **Maintainability concerns** (complex logic, unclear naming)

#### **💡 Recommended Improvements (Consider Fixing):**
- **Code style consistency** (indentation, formatting)
- **Documentation improvements** (better comments, docstrings)
- **Minor optimizations** (redundant code, simplifications)

#### **ℹ️ Informational (Optional):**
- **Best practice suggestions** that don't affect functionality
- **Alternative approaches** that could be considered
- **Future enhancement opportunities**

### **Decision Matrix**

**If Critical Issues Found (≥1):**
- **Action**: Implement all critical fixes immediately
- **Rationale**: Security and functionality must not be compromised

**If Many Issues Found (>3-5 total):**
- **Action**: Use `gh pr view` to implement fixes programmatically
- **Rationale**: Efficient batch processing of multiple changes

**If Few Issues Found (≤3 total):**
- **Action**: Manual review and selective implementation
- **Rationale**: Quick targeted fixes for specific concerns

**If Clean Review (minimal/no issues):**
- **Action**: Proceed with merge following proper order
- **Rationale**: Code quality standards met

### **Implementation Workflow**

**For Critical/Many Issues:**
```bash
# 1. Navigate to appropriate submodule
cd /home/jason/projects/jpotterlabs/trendit/[submodule]

# 2. Ensure on correct feature branch
git status && git branch

# 3. Implement fixes (use checkpoint before changes)
# 4. Test fixes locally
# 5. Commit improvements
git add . && git commit -m "Address CodeRabbit review feedback

- Fix security issues (add rel='noopener' to external links)
- Resolve code quality concerns (variable shadowing, etc.)
- Improve code consistency and maintainability

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 6. Push updates
git push
```

### **Assessment Example Template**

```markdown
## 📋 CodeRabbit Review Analysis for [Repository] PR #[Number]

### **✅ Issues to Address ([X] actionable items):**

**Critical Issues (Must Fix):**
- [Specific security/functionality issue with file:line reference]

**Should Fix:**
- [Code quality issue with file:line reference]

**Recommended:**
- [Style/optimization suggestion with file:line reference]

### **✅ Positive Findings:**
- [List approved patterns and good practices found]

### **Recommendation: [Action Decision]**
[Rationale for chosen approach based on issue severity and count]
```

### **Quality Gates**

Before proceeding with merge:
- [ ] **All critical issues resolved**
- [ ] **Security vulnerabilities addressed**
- [ ] **Code quality standards met**
- [ ] **No production deployment blockers**
- [ ] **Changes tested and verified**

### **Merge Order (Post-Review)**

After CodeRabbit assessment and fixes:
1. **Backend Submodule PR** - merge first
2. **Frontend Submodule PR** - merge second
3. **Root Repository PR** - merge third and cleanup

This systematic approach ensures:
- ✅ **Consistent code quality** across all deployments
- ✅ **Security standards** maintained
- ✅ **Efficient review processing** based on issue complexity
- ✅ **Clear decision criteria** for merge readiness

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

## API Testing & Verification

### Admin Test User Endpoint
For reliable API testing, use the admin endpoint (requires `ADMIN_SECRET_KEY`):

```bash
# Create/reset test user
curl -X POST "https://api.potterlabs.xyz/auth/create-test-user" \
  -H "Content-Type: application/json" \
  -d '{"admin_key": "YOUR_ADMIN_SECRET_KEY"}'

# Response includes consistent test credentials
{
  "user": {
    "email": "test@trendit.dev",
    "password": "TestPassword123"
  },
  "api_key": "tk_ABC123..."
}
```

### Testing Workflow
```bash
# 1. Get test credentials
RESPONSE=$(curl -s -X POST "https://api.potterlabs.xyz/auth/create-test-user" \
  -H "Content-Type: application/json" \
  -d '{"admin_key": "YOUR_ADMIN_KEY"}')

# 2. Extract API key
API_KEY=$(echo "$RESPONSE" | jq -r '.api_key')

# 3. Test any gated endpoint
curl -X GET "https://api.potterlabs.xyz/api/scenarios/1/subreddit-keyword-search?subreddit=python&keywords=test&date_from=2024-01-01&date_to=2024-12-31&limit=1" \
  -H "Authorization: Bearer $API_KEY"
```

### Verification Checklist

Before making changes:
- [ ] Verify current working directory with `pwd`
- [ ] Check git repository with `git remote -v`
- [ ] Confirm branch state with `git status`
- [ ] Test endpoints work with fresh API key

After making changes:
- [ ] Run appropriate linting: `npm run lint` or `ruff` (if available)
- [ ] Test changed functionality with admin test user
- [ ] Verify both JWT and API key authentication still work
- [ ] Check that submodule pointer updates correctly in root repo

## Troubleshooting

### Common Issues & Solutions

**"Not authenticated" errors:**
1. Check API key format (must start with `tk_`)
2. Verify user has ACTIVE subscription status
3. Check usage limits (free tier: 100 calls/month)
4. Ensure API key is not expired

**Git submodule confusion:**
1. Always use `pwd` before git operations
2. Use absolute paths for navigation
3. Fix detached HEAD immediately: `git checkout main`
4. Verify with `git remote -v` which repo you're in

**Directory navigation issues:**
1. Bash maintains working directory across commands
2. Use absolute paths: `/home/jason/projects/jpotterlabs/trendit/backend`
3. Never assume relative paths will work
4. Always verify location before operations

**Deployment verification:**
1. Check environment variables are set on production
2. Test admin endpoint responds with 403 for wrong key
3. Verify submodule updates are reflected in deployment
4. Test both new and existing functionality
