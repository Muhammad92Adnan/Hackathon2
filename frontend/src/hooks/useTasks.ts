// src/hooks/useTasks.ts
'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '@/lib/types';

export const useTasks = (userId: number) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async (status?: 'all' | 'pending' | 'completed') => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.getTasks(userId, status);
      setTasks(response.data);
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (title: string, description?: string) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.createTask(userId, title, description);
      setTasks(prev => [response.data, ...prev]);
      return response.data;
    } catch (err) {
      setError('Failed to create task');
      console.error('Error creating task:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateTask = async (taskId: number, data: UpdateTaskRequest) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.updateTask(userId, taskId, data);
      setTasks(prev => prev.map(task => task.id === taskId ? response.data : task));
      return response.data;
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (taskId: number, completed: boolean) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.toggleTaskCompletion(userId, taskId, completed);
      setTasks(prev => prev.map(task => task.id === taskId ? response.data : task));
      return response.data;
    } catch (err) {
      setError('Failed to toggle task completion');
      console.error('Error toggling task completion:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = async (taskId: number) => {
    try {
      setLoading(true);
      setError(null);
      await apiClient.deleteTask(userId, taskId);
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    toggleTaskCompletion,
    deleteTask,
  };
};