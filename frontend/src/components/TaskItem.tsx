// src/components/TaskItem.tsx
import { useState } from 'react';
import { Task, UpdateTaskRequest } from '@/lib/types';
import { useTasks } from '@/hooks/useTasks';

interface TaskItemProps {
  task: Task;
  userId: number;
}

export const TaskItem = ({ task, userId }: TaskItemProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description);
  const [error, setError] = useState<string | null>(null);
  
  const { updateTask, toggleTaskCompletion, deleteTask, loading } = useTasks(userId);

  const handleToggle = async () => {
    try {
      await toggleTaskCompletion(task.id, !task.completed);
    } catch (err) {
      console.error('Error toggling task:', err);
    }
  };

  const handleEdit = async () => {
    if (!editTitle.trim()) {
      setError('Title is required');
      return;
    }

    try {
      const updateData: UpdateTaskRequest = {
        title: editTitle.trim(),
        description: editDescription.trim(),
      };
      await updateTask(task.id, updateData);
      setIsEditing(false);
      setError(null);
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleCancel = () => {
    setEditTitle(task.title);
    setEditDescription(task.description);
    setIsEditing(false);
    setError(null);
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(task.id);
      } catch (err) {
        console.error('Error deleting task:', err);
      }
    }
  };

  return (
    <li className={`border rounded-lg p-4 mb-2 ${task.completed ? 'bg-green-50' : 'bg-white'}`}>
      {isEditing ? (
        <div className="space-y-4">
          <div>
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="w-full p-2 border rounded mb-2"
              maxLength={200}
            />
            {error && <p className="text-red-500 text-sm">{error}</p>}
          </div>
          <div>
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="w-full p-2 border rounded"
              rows={3}
              maxLength={1000}
            />
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handleEdit}
              disabled={loading}
              className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              disabled={loading}
              className="px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600 disabled:opacity-50"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="flex items-start">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggle}
            className="mt-1 mr-3 h-5 w-5 text-indigo-600 rounded"
          />
          <div className="flex-1 min-w-0">
            <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`mt-1 text-sm ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                {task.description}
              </p>
            )}
            <p className="mt-1 text-xs text-gray-400">
              Created: {new Date(task.created_at).toLocaleDateString()}
            </p>
          </div>
          <div className="flex space-x-2 ml-4">
            <button
              onClick={() => setIsEditing(true)}
              className="text-blue-500 hover:text-blue-700"
              title="Edit task"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
            </button>
            <button
              onClick={handleDelete}
              className="text-red-500 hover:text-red-700"
              title="Delete task"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </li>
  );
};