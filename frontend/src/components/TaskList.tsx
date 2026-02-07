// src/components/TaskList.tsx
import { Task } from '@/lib/types';
import { TaskItem } from '@/components/TaskItem';

interface TaskListProps {
  tasks: Task[];
  userId: number;
  loading: boolean;
  error: string | null;
}

export const TaskList = ({ tasks, userId, loading, error }: TaskListProps) => {
  if (loading) {
    return (
      <div className="text-center py-8">
        <p>Loading tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <span className="block sm:inline">{error}</span>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No tasks yet. Add your first task!</p>
      </div>
    );
  }

  return (
    <ul className="divide-y divide-gray-200">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} userId={userId} />
      ))}
    </ul>
  );
};