# Research: Phase II Web-Based Todo Application

**Date**: 2026-02-08
**Branch**: 002-web-todo
**Purpose**: Document technical decisions, best practices, and alternatives for Phase II implementation

## Research Questions & Decisions

### 1. Better Auth JWT Plugin Integration

**Question**: How should Better Auth with JWT plugin be configured for frontend-backend communication?

**Decision**: Use Better Auth's JWT plugin on frontend to issue tokens, validate on backend using shared secret

**Rationale**:
- Better Auth JWT plugin provides industry-standard JWT token generation
- Shared BETTER_AUTH_SECRET enables backend to verify tokens without calling back to frontend
- Stateless authentication - backend can validate tokens independently
- Follows OAuth2/JWT best practices for SPAs and APIs

**Implementation Details**:
- Frontend: Install `better-auth` and configure JWT plugin in `src/lib/auth.ts`
- Backend: Use `python-jose` or `PyJWT` to verify JWT signature with shared secret
- Token payload includes: `user_id`, `email`, `exp` (expiration), `iat` (issued at)
- Frontend stores JWT in localStorage or sessionStorage
- Frontend includes token in `Authorization: Bearer <token>` header for all API calls

**Alternatives Considered**:
- Session-based auth with cookies: Rejected - requires backend session storage, less scalable
- OAuth2 Authorization Code Flow: Rejected - overkill for single-app authentication
- Magic links: Rejected - not in Phase II requirements

**References**:
- Better Auth JWT Plugin: https://better-auth.com/docs/plugins/jwt
- FastAPI JWT authentication: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

---

### 2. API Endpoint Design with User ID in Path

**Question**: Should user_id be in the URL path (`/api/{user_id}/tasks`) or query parameter?

**Decision**: Include user_id in URL path as required by specification

**Rationale**:
- RESTful design - user_id is a resource identifier, belongs in path
- Explicit authorization check - backend MUST verify path user_id matches JWT user_id
- Clear API structure - `/api/{user_id}/tasks` makes ownership explicit
- Prevents accidental cross-user data access

**Implementation Details**:
- All task endpoints: `/api/{user_id}/tasks`, `/api/{user_id}/tasks/{task_id}`
- JWT middleware extracts user_id from token claims
- Path parameter validation: `if path_user_id != jwt_user_id: raise HTTPException(403)`
- FastAPI path parameters: `@app.get("/api/{user_id}/tasks")`

**Alternatives Considered**:
- User ID only in JWT: Rejected - less explicit, spec requires user_id in path
- Query parameter: Rejected - not RESTful for resource identifiers
- No user_id in path, infer from JWT: Rejected - spec explicitly defines API structure

---

### 3. Task Filtering Implementation

**Question**: Should task filtering (all/pending/completed) be client-side or server-side?

**Decision**: Client-side filtering for Phase II, server-side optimization in future phases

**Rationale**:
- Phase II scope: Users expected to have <1000 tasks, client-side filtering is fast
- Simplicity: No additional backend logic needed for Phase II
- Performance: Modern browsers handle filtering hundreds of items instantly
- Future-proof: API supports `?status=` query parameter for server-side filtering later

**Implementation Details**:
- Frontend: Filter tasks array based on `completed` boolean after fetching
- React state: `const [filter, setFilter] = useState<'all'|'pending'|'completed'>('all')`
- Filtering logic: `tasks.filter(t => filter === 'all' || (filter === 'pending' && !t.completed) || (filter === 'completed' && t.completed))`
- Backend: API supports optional `?status=all|pending|completed` query parameter for future use

**Alternatives Considered**:
- Server-side filtering from start: Rejected - premature optimization, adds backend complexity
- No filtering: Rejected - spec requires task filtering feature

---

### 4. Database Schema and Migrations

**Question**: How should database schema be managed and migrated for Neon PostgreSQL?

**Decision**: Use SQLModel for schema definition with Alembic for migrations

**Rationale**:
- SQLModel combines Pydantic validation with SQLAlchemy ORM
- Type safety: Python type hints translate to database types
- Alembic provides robust migration framework
- Neon PostgreSQL is fully compatible with standard PostgreSQL tools

**Implementation Details**:
- Define models: `User(SQLModel, table=True)` and `Task(SQLModel, table=True)`
- Foreign key: `user_id: int = Field(foreign_key="user.id")`
- Indexes: `email` (unique), `user_id + created_at` for task queries
- Alembic commands: `alembic init`, `alembic revision --autogenerate`, `alembic upgrade head`
- Connection string: `postgresql://user:pass@neon.tech/db?sslmode=require`

**Alternatives Considered**:
- Raw SQL migrations: Rejected - no type safety, harder to maintain
- Django ORM: Rejected - not compatible with FastAPI ecosystem
- No migrations (manual schema): Rejected - not maintainable for production

**References**:
- SQLModel: https://sqlmodel.tiangolo.com/
- Alembic: https://alembic.sqlalchemy.org/

---

### 5. CORS Configuration for Frontend-Backend Communication

**Question**: How should CORS be configured to allow Next.js frontend to call FastAPI backend?

**Decision**: Configure FastAPI CORS middleware to allow frontend origin with credentials

**Rationale**:
- Security: Explicit origin whitelist prevents unauthorized domains
- Credentials: Required for JWT token in Authorization header
- Development vs Production: Different origins for local dev and deployed apps

**Implementation Details**:
```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",  # Next.js dev server
    "https://yourdomain.vercel.app",  # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Alternatives Considered**:
- Allow all origins (`*`): Rejected - security risk
- No CORS: Rejected - browsers block cross-origin requests
- Proxy through Next.js: Rejected - adds latency and complexity

---

### 6. Environment Variables and Secret Management

**Question**: What environment variables are needed and how should they be managed?

**Decision**: Use .env files locally, platform environment variables in production

**Environment Variables**:

**Frontend (.env.local)**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<shared-secret-min-32-chars>
BETTER_AUTH_URL=http://localhost:3000
```

**Backend (.env)**:
```
DATABASE_URL=postgresql://user:pass@neon.tech/db?sslmode=require
BETTER_AUTH_SECRET=<same-as-frontend>
CORS_ORIGINS=http://localhost:3000,https://yourdomain.vercel.app
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**Rationale**:
- BETTER_AUTH_SECRET must be identical on frontend and backend
- DATABASE_URL contains sensitive Neon credentials
- NEXT_PUBLIC_* prefix makes variables accessible in browser
- Separate .env files for frontend and backend isolation

**Implementation Details**:
- Create .env.example files with placeholder values
- Add .env to .gitignore
- Vercel: Set environment variables in project settings
- Railway/Render: Set environment variables in dashboard
- Generate BETTER_AUTH_SECRET: `openssl rand -base64 32`

**Alternatives Considered**:
- Hardcoded secrets: Rejected - security violation
- Single .env file: Rejected - frontend and backend have different variables
- Cloud secret managers (AWS Secrets Manager): Rejected - overkill for Phase II

---

### 7. Testing Strategy

**Question**: What testing approach should be used for frontend and backend?

**Decision**: Pytest for backend, Vitest for frontend, Playwright for E2E

**Backend Testing (pytest)**:
- Unit tests: Models, services (business logic)
- Integration tests: API endpoints with test database
- Fixtures: `conftest.py` for test client, test database
- Coverage goal: >80% for critical paths (auth, task CRUD)

**Frontend Testing (Vitest + React Testing Library)**:
- Unit tests: Components, hooks, utility functions
- Integration tests: User flows (login, add task, filter)
- Mocking: API calls with MSW (Mock Service Worker)

**E2E Testing (Playwright)**:
- Critical user flows: Signup → Login → Add Task → Filter → Logout
- Cross-browser: Chrome, Firefox, Safari
- Run before deployment

**Rationale**:
- Pytest is Python standard, integrates well with FastAPI
- Vitest is faster than Jest, better TypeScript support
- Playwright provides reliable E2E testing with good Next.js support

**Alternatives Considered**:
- Jest for frontend: Rejected - Vitest is faster and better for Vite/Next.js
- Selenium for E2E: Rejected - Playwright is more modern and reliable
- No E2E tests: Rejected - critical user flows need E2E coverage

---

### 8. Deployment Strategy

**Question**: Where and how should frontend and backend be deployed?

**Decision**: Vercel for frontend, Railway for backend, Neon for database

**Frontend (Vercel)**:
- Automatic deployment from Git push
- Edge network for fast global access
- Automatic HTTPS
- Environment variables configured in dashboard
- Build command: `npm run build`
- Output directory: `.next`

**Backend (Railway)**:
- Automatic deployment from Git push
- Internal networking for database connection
- Automatic HTTPS
- Environment variables configured in dashboard
- Start command: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

**Database (Neon PostgreSQL)**:
- Serverless PostgreSQL with auto-scaling
- Connection pooling built-in
- Automatic backups
- Dashboard for schema management

**Rationale**:
- Vercel specializes in Next.js deployments
- Railway provides easy Python/FastAPI deployment
- Neon offers serverless PostgreSQL with generous free tier
- All platforms support automatic HTTPS and environment variables

**Alternatives Considered**:
- Render for backend: Valid alternative (user can choose Railway or Render per spec)
- Heroku: Rejected - less generous free tier, deprecated free plans
- Self-hosted VPS: Rejected - too much operational overhead for hackathon

---

## Best Practices Summary

### Security
- ✅ All secrets in environment variables
- ✅ JWT tokens with expiration (24 hours)
- ✅ HTTPS in production (automatic via Vercel/Railway)
- ✅ Password hashing via Better Auth
- ✅ User ID validation on every API request
- ✅ CORS configured with explicit origins

### Code Quality
- ✅ TypeScript for type safety (frontend)
- ✅ Type hints with Pydantic/SQLModel (backend)
- ✅ Docstrings for all functions and classes
- ✅ Descriptive variable and function names
- ✅ Separate concerns: models, services, API routes

### Performance
- ✅ Database indexes on email and user_id
- ✅ Connection pooling (Neon built-in)
- ✅ Client-side filtering for <1000 tasks
- ✅ Lazy loading for React components

### Maintainability
- ✅ Monorepo structure for related code
- ✅ Consistent error handling
- ✅ Comprehensive testing (unit + integration + E2E)
- ✅ README files for setup instructions
- ✅ .env.example files for onboarding

---

## Technology Decisions Summary

| Category | Technology | Rationale |
|----------|-----------|-----------|
| Frontend Framework | Next.js 16+ (App Router) | Modern React framework, server components, excellent developer experience |
| Frontend Language | TypeScript | Type safety, better IDE support, catches errors at compile time |
| Frontend Styling | Tailwind CSS | Utility-first, fast development, responsive design out of the box |
| Frontend Auth | Better Auth + JWT Plugin | Industry-standard authentication, JWT token generation |
| Frontend State | React Hooks (useState, useEffect) | Simple, built-in, sufficient for Phase II scope |
| Backend Framework | FastAPI | Fast, modern, async support, automatic API docs, Python 3.13+ |
| Backend ORM | SQLModel | Type-safe, combines Pydantic + SQLAlchemy, excellent FastAPI integration |
| Backend Validation | Pydantic | Automatic request/response validation, integrated with FastAPI |
| Backend Auth | PyJWT / python-jose | JWT token verification, industry-standard library |
| Database | Neon PostgreSQL | Serverless, auto-scaling, generous free tier, PostgreSQL compatible |
| Database Migrations | Alembic | Industry-standard, works with SQLModel/SQLAlchemy |
| Backend Testing | pytest + httpx | Async support, test client for FastAPI, extensive plugin ecosystem |
| Frontend Testing | Vitest + React Testing Library | Fast, TypeScript support, React-friendly assertions |
| E2E Testing | Playwright | Reliable, cross-browser, good Next.js support |
| Frontend Deployment | Vercel | Next.js specialists, automatic deployments, global CDN |
| Backend Deployment | Railway (or Render) | Easy Python deployment, automatic HTTPS, database integration |

---

## Open Questions / Future Considerations

1. **Password Reset**: Not in Phase II - defer to Phase III or later
2. **Email Verification**: Not in Phase II - users can register without email verification
3. **Multi-device Sessions**: Not in Phase II - single JWT token per user
4. **Real-time Updates**: Not in Phase II - polling or manual refresh for now
5. **Server-side Task Filtering**: Implemented as API feature but not required in Phase II
6. **Rate Limiting**: Not in Phase II - consider for production deployment
7. **Logging and Monitoring**: Basic console logs for Phase II, consider structured logging later
8. **CI/CD Pipeline**: Manual testing for Phase II, consider GitHub Actions later

---

**Research Complete**: All technical decisions documented and ready for Phase 1 design artifacts.
