# Trendit - Reddit Data Collection Platform

A modern, microservices-based Reddit data collection and analysis platform with Auth0 OAuth integration.

## 🏗️ Architecture

This repository orchestrates the complete Trendit platform using git submodules:

```
trendit/
├── backend/     → jpotterlabs/trendit-backend   (FastAPI + Auth0)
├── frontend/    → jpotterlabs/trendit-frontend  (Next.js + Auth0 OAuth)
├── mobile/      → jpotterlabs/trendit-mobile    (React Native + Auth0)
└── docs/        → Documentation and deployment guides
```

## 🚀 Quick Start

### 1. Clone with Submodules
```bash
git clone --recursive https://github.com/jpotterlabs/trendit.git
cd trendit

# Or if already cloned:
git submodule update --init --recursive
```

### 2. Development Setup
```bash
# Start backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload --port 8000

# Start frontend (new terminal)
cd frontend
npm install
npm run dev

# Start mobile (new terminal - optional)
cd mobile
npm install
npm run ios    # or npm run android
```

### 3. Production Deployment
Each component can be deployed independently:

**Backend Options:**
- Docker containers on AWS/GCP/Azure
- Serverless functions (AWS Lambda, Google Cloud Functions)
- Traditional VPS hosting

**Frontend Options:**  
- Vercel (recommended for Next.js)
- Netlify static hosting
- AWS S3 + CloudFront
- Docker containers

**Mobile Options:**
- Apple App Store (iOS)
- Google Play Store (Android)
- TestFlight (iOS beta testing)
- Firebase App Distribution (cross-platform testing)

## 🔧 Configuration

### Backend Configuration
```bash
cd backend
cp .env.example .env
# Configure database, Reddit API, Auth0 credentials
```

### Frontend Configuration  
```bash
cd frontend  
cp .env.example .env.local
# Configure API URL and Auth0 settings
```

## 🌟 Features

### Authentication & Authorization
- **Auth0 OAuth Integration** - Google and GitHub social login
- **Traditional Auth** - Email/password registration and login
- **JWT Tokens** - Secure API authentication
- **API Keys** - Programmatic access control

### Reddit Data Collection
- **Async Collection** - High-performance data gathering
- **Multi-Subreddit Support** - Collect from multiple sources
- **Advanced Filtering** - Date ranges, scores, keywords
- **Background Jobs** - Progress tracking for large collections

### Analytics & Export
- **Sentiment Analysis** - AI-powered text analysis
- **Engagement Metrics** - Comprehensive post and comment analytics
- **Multi-Format Export** - CSV, JSON, Parquet support
- **Real-time Dashboards** - Live data visualization

### Billing & Subscriptions
- **Paddle Integration** - Complete payment processing
- **Multi-tier Pricing** - Free, Pro, Enterprise plans
- **Usage Tracking** - Real-time API call monitoring
- **Rate Limiting** - Tier-based access controls

## 📊 Independent Deployment

Each microservice can be deployed completely independently:

### Backend Standalone
```bash
cd backend
docker build -t trendit-backend .
docker run -p 8000:8000 trendit-backend
```

### Frontend Standalone
```bash
cd frontend
npm run build
npm start
# Or deploy to Vercel: vercel --prod
```

## 🔒 Security

- **No Shared Secrets** - Each service manages its own credentials
- **Environment-Based Config** - All secrets via environment variables
- **Auth0 JWT Verification** - Secure token validation
- **CORS Configuration** - Proper cross-origin handling

## 📚 Documentation

- **[Backend Documentation](backend/README.md)** - FastAPI setup and API reference
- **[Frontend Documentation](frontend/README.md)** - Next.js setup and deployment
- **[Auth0 Setup Guide](frontend/AUTH0_SETUP_GUIDE.md)** - Complete OAuth configuration
- **[Architecture Overview](frontend/AUTH0_ARCHITECTURE.md)** - System design principles
- **[Deployment Checklist](frontend/DEPLOYMENT_CHECKLIST.md)** - Production deployment steps

## 🛠️ Development Workflow

### Working with Submodules
```bash
# Update submodules to latest
git submodule update --remote

# Make changes in a submodule
cd backend
# ... make changes ...
git add . && git commit -m "backend changes"
git push

# Update main repo to point to new commit
cd ..
git add backend
git commit -m "Update backend submodule"
git push
```

### Independent Development
```bash
# Work directly on backend repo
git clone https://github.com/jpotterlabs/trendit-backend.git
cd trendit-backend
# ... develop and deploy independently ...

# Work directly on frontend repo
git clone https://github.com/jpotterlabs/trendit-frontend.git  
cd trendit-frontend
# ... develop and deploy independently ...
```

## 🌍 Deployment Scenarios

### Scenario 1: Full Microservices
- Backend: AWS ECS containers
- Frontend: Vercel global CDN
- Database: AWS RDS PostgreSQL
- Auth: Auth0 SaaS

### Scenario 2: Cost-Optimized
- Backend: Single VPS with Docker
- Frontend: Netlify static hosting
- Database: Self-hosted PostgreSQL
- Auth: Auth0 free tier

### Scenario 3: Enterprise
- Backend: Kubernetes cluster
- Frontend: Enterprise CDN
- Database: High-availability PostgreSQL
- Auth: Auth0 Enterprise

## 📈 Scaling Strategy

- **Horizontal Scaling** - Each service scales independently
- **Database Sharding** - Separate databases per service if needed
- **CDN Distribution** - Global frontend delivery
- **Caching Layers** - Redis for API response caching
- **Load Balancing** - Multiple backend instances

## 🆘 Support

For issues:
1. **Backend Issues** - Check [trendit-backend repository](https://github.com/jpotterlabs/trendit-backend)
2. **Frontend Issues** - Check [trendit-frontend repository](https://github.com/jpotterlabs/trendit-frontend)
3. **Integration Issues** - File issues in this main repository
4. **Auth0 Setup** - See [Auth0 Setup Guide](frontend/AUTH0_SETUP_GUIDE.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with modern microservices architecture for maximum scalability, portability, and deployment flexibility.**