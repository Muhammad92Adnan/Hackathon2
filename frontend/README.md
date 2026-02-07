# Phase II Todo Application - Frontend

Next.js 16+ web application with Better Auth JWT authentication and Tailwind CSS.

## Technology Stack

- **Framework**: Next.js 16+ (App Router)
- **UI Library**: React 19+
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT plugin
- **HTTP Client**: Axios
- **Forms**: React Hook Form

## Setup Instructions

### Prerequisites

- Node.js 20.x or later
- npm, yarn, or pnpm

### Local Development

1. **Install dependencies**:
   ```bash
   npm install
   # Or: yarn install
   # Or: pnpm install
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your actual values:
   # - NEXT_PUBLIC_API_URL (backend API URL)
   # - BETTER_AUTH_SECRET (same as backend - must match!)
   # - BETTER_AUTH_URL (this frontend URL)
   ```

3. **Start development server**:
   ```bash
   npm run dev
   # Or: yarn dev
   # Or: pnpm dev
   ```

4. **Access application**:
   - Frontend: http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── app/                # Next.js App Router
│   │   ├── (auth)/         # Auth routes group
│   │   │   ├── login/
│   │   │   └── signup/
│   │   ├── dashboard/      # Protected dashboard
│   │   ├── layout.tsx      # Root layout
│   │   └── page.tsx        # Landing page
│   ├── components/         # React components
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   ├── TaskFilter.tsx
│   │   ├── Header.tsx
│   │   └── SignupForm.tsx
│   ├── hooks/              # Custom React hooks
│   │   ├── useAuth.ts
│   │   └── useTasks.ts
│   └── lib/                # Utilities
│       ├── auth.ts         # Better Auth config
│       ├── api.ts          # API client
│       └── types.ts        # TypeScript types
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── .env.local.example
└── README.md
```

## Development

### Adding New Pages

Create page files in `src/app/`:
```typescript
// src/app/your-page/page.tsx
export default function YourPage() {
  return <div>Your content</div>;
}
```

### Adding New Components

Create component files in `src/components/`:
```typescript
// src/components/YourComponent.tsx
export function YourComponent() {
  return <div>Your component</div>;
}
```

### Using Authentication

```typescript
import { useAuth } from '@/hooks/useAuth';

function MyComponent() {
  const { user, login, logout, isAuthenticated } = useAuth();

  // Access user data or call auth methods
}
```

### Making API Calls

```typescript
import { apiClient } from '@/lib/api';

async function fetchData() {
  const response = await apiClient.get('/api/1/tasks');
  return response.data;
}
```

## Building for Production

```bash
npm run build
npm run start
```

## Deployment

See main project README for deployment instructions to Vercel.

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API base URL (public, can be accessed in browser)
- `BETTER_AUTH_SECRET` - Shared secret for JWT verification (must match backend)
- `BETTER_AUTH_URL` - This frontend's URL for Better Auth callbacks

**IMPORTANT**: `BETTER_AUTH_SECRET` must be identical between frontend and backend!

## Features

- User registration and login
- JWT-based authentication with token persistence
- Protected routes (automatic redirect to login)
- Task CRUD operations (Create, Read, Update, Delete)
- Task completion toggling
- Task filtering (All, Pending, Completed)
- Responsive design (mobile and desktop)
- Error handling and loading states
