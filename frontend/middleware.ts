// middleware.ts
import { NextRequest, NextResponse } from 'next/server';

// Protected routes that require authentication
const protectedRoutes = ['/dashboard'];

export function middleware(request: NextRequest) {
  // Check if the route is protected
  const isProtectedRoute = protectedRoutes.some(route => 
    request.nextUrl.pathname.startsWith(route)
  );

  if (isProtectedRoute) {
    // Check if user is authenticated by looking for the token in localStorage
    // Note: In a real Next.js middleware, we can't access localStorage directly
    // This is a simplified version - in practice, tokens would be stored in cookies
    const token = request.cookies.get('access_token')?.value || 
                  request.headers.get('authorization')?.split(' ')[1];

    if (!token) {
      // Redirect to login if not authenticated
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  return NextResponse.next();
}

// Specify which paths the middleware should run for
export const config = {
  matcher: ['/dashboard/:path*'],
};