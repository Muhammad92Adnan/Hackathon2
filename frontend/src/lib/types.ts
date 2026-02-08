// src/lib/types.ts

export interface User {
  id: number;
  email: string;
  created_at: string; // ISO 8601 datetime string
}

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string; // ISO 8601 datetime string
  updated_at: string; // ISO 8601 datetime string
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

export type TaskFilter = 'all' | 'pending' | 'completed';

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
}