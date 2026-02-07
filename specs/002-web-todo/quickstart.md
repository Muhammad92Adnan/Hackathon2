# Quickstart Guide: Phase II Web-Based Todo Application

**Date**: 2026-02-08
**Branch**: 002-web-todo
**Purpose**: Step-by-step setup instructions for local development and deployment

## Prerequisites

### Required Software

- **Node.js**: v20.x or later (for Next.js 16+)
- **Python**: 3.13 or later (for FastAPI backend)
- **uv**: Python package manager (install with `pip install uv`)
- **Git**: For version control
- **PostgreSQL Client**: For database management (optional but helpful)

### Cloud Accounts

- **Neon**: PostgreSQL database (https://neon.tech) - Free tier available
- **Vercel**: Frontend deployment (https://vercel.com) - Free tier available
- **Railway** or **Render**: Backend deployment - Free tier available

---

## Local Development Setup

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd h2p1
git checkout 002-web-todo
```

### Step 2: Backend Setup

#### 2.1 Navigate to Backend Directory

```bash
cd backend
```

#### 2.2 Create Virtual Environment

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Or using standard Python
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 2.3 Install Dependencies

```bash
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

#### 2.4 Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
# backend/.env
DATABASE_URL=postgresql://user:password@your-neon-host/dbname?sslmode=require
BETTER_AUTH_SECRET=<generate-random-32-char-secret>
CORS_ORIGINS=http://localhost:3000
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**Generate BETTER_AUTH_SECRET**:
```bash
# Linux/macOS
openssl rand -base64 32

# Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

#### 2.5 Setup Database

Create Neon PostgreSQL database:
1. Sign up at https://neon.tech
2. Create new project
3. Copy connection string to `.env` as `DATABASE_URL`

Run migrations:
```bash
# Initialize Alembic (first time only)
alembic init src/db/migrations

# Create initial migration
alembic revision --autogenerate -m "Create user and task tables"

# Apply migration
alembic upgrade head
```

#### 2.6 Run Backend Server

```bash
# Development server with auto-reload
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs (Swagger UI)
```

---

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend Directory

```bash
cd ../frontend  # From backend/ directory
# Or from repo root: cd frontend
```

#### 3.2 Install Dependencies

```bash
npm install
# Or use yarn: yarn install
# Or use pnpm: pnpm install
```

#### 3.3 Configure Environment Variables

Create `.env.local` file in `frontend/` directory:

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<same-secret-as-backend>
BETTER_AUTH_URL=http://localhost:3000
```

**IMPORTANT**: `BETTER_AUTH_SECRET` MUST be identical to backend `.env`

#### 3.4 Run Frontend Server

```bash
npm run dev
# Or: yarn dev
# Or: pnpm dev

# Server runs at http://localhost:3000
```

---

### Step 4: Verify Setup

1. **Backend Health Check**:
   - Visit http://localhost:8000/docs
   - You should see Swagger UI with API documentation

2. **Frontend Health Check**:
   - Visit http://localhost:3000
   - You should see the landing page

3. **End-to-End Test**:
   - Click "Sign Up" on frontend
   - Create a new account (email + password)
   - Log in with credentials
   - Add a new task
   - Verify task appears in list
   - Toggle task completion
   - Filter tasks (All / Pending / Completed)
   - Log out

---

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py

# Run integration tests only
pytest tests/integration/
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm test
# Or: npm run test:unit

# Run E2E tests (requires both frontend and backend running)
npm run test:e2e

# Run tests in watch mode
npm test -- --watch
```

---

## Deployment

### Deploy Backend to Railway

1. **Create Railway Account**: https://railway.app
2. **Create New Project**: "New Project" → "Deploy from GitHub repo"
3. **Select Repository**: Choose your GitHub repository
4. **Configure Environment Variables**:
   - Go to project settings → Variables
   - Add all variables from `backend/.env`:
     - `DATABASE_URL` (from Neon)
     - `BETTER_AUTH_SECRET`
     - `CORS_ORIGINS` (update to production frontend URL)
     - `JWT_ALGORITHM=HS256`
     - `JWT_EXPIRATION_HOURS=24`
5. **Configure Start Command**:
   - Settings → Deploy → Start Command:
     ```
     uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
     ```
6. **Deploy**: Railway auto-deploys on git push
7. **Get URL**: Copy the Railway-provided URL (e.g., `https://yourapp.railway.app`)

**Alternative: Deploy to Render**
- Similar process at https://render.com
- Create Web Service → Connect GitHub repo
- Add environment variables
- Deploy

### Deploy Frontend to Vercel

1. **Create Vercel Account**: https://vercel.com
2. **Import Project**: "Add New" → "Project" → "Import Git Repository"
3. **Configure Framework**: Vercel auto-detects Next.js
4. **Configure Environment Variables**:
   - Settings → Environment Variables
   - Add variables from `frontend/.env.local`:
     - `NEXT_PUBLIC_API_URL` (use Railway/Render backend URL)
     - `BETTER_AUTH_SECRET` (same as backend)
     - `BETTER_AUTH_URL` (use Vercel-provided URL after first deploy)
5. **Deploy**: Vercel auto-deploys on git push to main branch
6. **Get URL**: Copy the Vercel-provided URL (e.g., `https://yourapp.vercel.app`)

### Update CORS Origins

After deployment, update backend `CORS_ORIGINS`:
```bash
# In Railway/Render environment variables
CORS_ORIGINS=http://localhost:3000,https://yourapp.vercel.app
```

---

## Environment Variables Reference

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | Neon PostgreSQL connection string | `postgresql://user:pass@host/db?sslmode=require` |
| BETTER_AUTH_SECRET | Shared secret for JWT verification (min 32 chars) | `<random-base64-string>` |
| CORS_ORIGINS | Comma-separated allowed origins | `http://localhost:3000,https://app.vercel.app` |
| JWT_ALGORITHM | JWT signing algorithm | `HS256` |
| JWT_EXPIRATION_HOURS | Token validity period | `24` |

### Frontend (.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Backend API base URL | `http://localhost:8000` (dev) or `https://api.railway.app` (prod) |
| BETTER_AUTH_SECRET | Shared secret (must match backend) | `<same-as-backend>` |
| BETTER_AUTH_URL | Frontend URL for Better Auth callbacks | `http://localhost:3000` (dev) or `https://app.vercel.app` (prod) |

---

## Common Issues & Troubleshooting

### Issue: "CORS policy" errors in browser console

**Solution**: Verify `CORS_ORIGINS` in backend `.env` includes frontend URL

### Issue: "Invalid JWT token" errors

**Solution**: Verify `BETTER_AUTH_SECRET` is identical in frontend and backend `.env`

### Issue: Database connection errors

**Solution**:
- Check `DATABASE_URL` format: `postgresql://user:password@host/dbname?sslmode=require`
- Verify Neon database is running (check Neon dashboard)
- Test connection: `psql $DATABASE_URL`

### Issue: Port already in use (3000 or 8000)

**Solution**: Kill process using port or use different port
```bash
# Linux/macOS
lsof -ti:3000 | xargs kill -9

# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process
```

### Issue: Frontend can't connect to backend

**Solution**:
- Verify backend is running (`http://localhost:8000/docs` accessible)
- Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
- Check browser network tab for actual error

---

## Development Workflow

### Feature Development

1. **Create feature branch**: `git checkout -b feature/your-feature`
2. **Write specs**: Update `specs/002-web-todo/spec.md` if needed
3. **Write tests**: Backend (`pytest`) and Frontend (Vitest/Playwright)
4. **Implement feature**: Follow TDD approach (tests first)
5. **Run tests**: Ensure all tests pass
6. **Commit**: `git commit -m "Add feature X"`
7. **Push**: `git push origin feature/your-feature`
8. **Deploy**: Merge to `002-web-todo` triggers auto-deploy

### Database Changes

1. **Update models**: Modify `backend/src/models/*.py`
2. **Generate migration**: `alembic revision --autogenerate -m "Description"`
3. **Review migration**: Check generated file in `src/db/migrations/versions/`
4. **Apply migration**: `alembic upgrade head`
5. **Test**: Verify changes in database

---

## Next Steps

After local setup is complete:

1. ✅ Verify all CRUD operations work (Create, Read, Update, Delete tasks)
2. ✅ Test authentication flow (Signup, Login, Logout)
3. ✅ Test task filtering (All, Pending, Completed)
4. ✅ Run full test suite (`pytest` + `npm test`)
5. ✅ Deploy to production (Vercel + Railway + Neon)
6. ✅ Record demo video (under 90 seconds)

---

**Quickstart Complete**: You're ready to develop Phase II features!

For detailed architecture and design decisions, see:
- [spec.md](spec.md) - Feature requirements
- [plan.md](plan.md) - Implementation plan
- [data-model.md](data-model.md) - Database schema
- [contracts/api-spec.yaml](contracts/api-spec.yaml) - API specification
