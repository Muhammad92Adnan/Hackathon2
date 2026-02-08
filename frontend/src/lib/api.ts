// src/lib/api.ts
import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include JWT token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle token expiration
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Clear token if unauthorized
          localStorage.removeItem('access_token');
          window.location.href = '/login'; // Redirect to login
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication endpoints
  async signup(email: string, password: string) {
    return this.client.post('/api/auth/signup', { email, password });
  }

  async signin(email: string, password: string) {
    return this.client.post('/api/auth/signin', { email, password });
  }

  async signout() {
    // Client-side logout - just remove the token
    localStorage.removeItem('access_token');
    return { message: 'Signed out successfully' };
  }

  // Task endpoints
  async getTasks(userId: number, status?: 'all' | 'pending' | 'completed') {
    const params = status && status !== 'all' ? { status } : {};
    return this.client.get(`/api/${userId}/tasks`, { params });
  }

  async createTask(userId: number, title: string, description?: string) {
    return this.client.post(`/api/${userId}/tasks`, { title, description });
  }

  async updateTask(userId: number, taskId: number, data: Partial<{ title: string; description: string; completed: boolean }>) {
    return this.client.put(`/api/${userId}/tasks/${taskId}`, data);
  }

  async toggleTaskCompletion(userId: number, taskId: number, completed: boolean) {
    return this.client.patch(`/api/${userId}/tasks/${taskId}/toggle`, { completed });
  }

  async deleteTask(userId: number, taskId: number) {
    return this.client.delete(`/api/${userId}/tasks/${taskId}`);
  }
}

export const apiClient = new ApiClient();