// src/app/dashboard/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';
import { TaskForm } from '@/components/TaskForm';
import { TaskList } from '@/components/TaskList';
import { TaskFilter } from '@/components/TaskFilter';

export default function DashboardPage() {
  const router = useRouter();
  const { user, loading: authLoading, isAuthenticated } = useAuth();
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const { tasks, loading: tasksLoading, error, fetchTasks } = useTasks(user?.id || 0);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    } else if (user) {
      fetchTasks(filter);
    }
  }, [authLoading, isAuthenticated, user, router, fetchTasks, filter]);

  const handleFilterChange = (newFilter: 'all' | 'pending' | 'completed') => {
    setFilter(newFilter);
  };

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Redirect handled by useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">My Tasks</h1>
          
          <TaskForm userId={user!.id} onTaskCreated={() => fetchTasks(filter)} />
          
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Tasks</h2>
            <TaskFilter onFilterChange={handleFilterChange} />
            <TaskList 
              tasks={tasks} 
              userId={user!.id} 
              loading={tasksLoading} 
              error={error} 
            />
          </div>
        </div>
      </main>
    </div>
  );
}