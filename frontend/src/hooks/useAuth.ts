// src/hooks/useAuth.ts
import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { User, AuthResponse, LoginRequest, SignupRequest } from '@/lib/types';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check if user is already logged in on component mount
    const token = localStorage.getItem('access_token');
    if (token) {
      const userData = localStorage.getItem('user_data');
      if (userData) {
        try {
          setUser(JSON.parse(userData));
        } catch (err) {
          console.error('Failed to parse user data:', err);
        }
      }
    }
    setLoading(false);
  }, []);

  const signup = async ({ email, password }: SignupRequest) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.signup(email, password);
      const { user: userData, access_token } = response.data as AuthResponse;
      
      // Store token and user data in localStorage
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_data', JSON.stringify(userData));
      
      setUser(userData);
      return { success: true, user: userData };
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Signup failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const login = async ({ email, password }: LoginRequest) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.signin(email, password);
      const { user: userData, access_token } = response.data as AuthResponse;
      
      // Store token and user data in localStorage
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_data', JSON.stringify(userData));
      
      setUser(userData);
      return { success: true, user: userData };
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Login failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      setLoading(true);
      await apiClient.signout();
      setUser(null);
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_data');
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setLoading(false);
    }
  };

  const isAuthenticated = !!user;

  return {
    user,
    loading,
    error,
    signup,
    login,
    logout,
    isAuthenticated,
  };
};