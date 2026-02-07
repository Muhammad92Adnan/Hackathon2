// src/components/Header.tsx
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';

export const Header = () => {
  const { user, logout, isAuthenticated } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <header className="bg-indigo-600 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold">
              Todo App
            </Link>
            <nav className="ml-6 flex space-x-4">
              {isAuthenticated && (
                <>
                  <Link href="/dashboard" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-700">
                    Dashboard
                  </Link>
                </>
              )}
            </nav>
          </div>
          <div className="flex items-center">
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm">Welcome, {user?.email}</span>
                <button
                  onClick={handleLogout}
                  className="px-3 py-2 rounded-md text-sm font-medium bg-indigo-700 hover:bg-indigo-800"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex space-x-4">
                <Link href="/login" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-700">
                  Login
                </Link>
                <Link href="/signup" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-700">
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};