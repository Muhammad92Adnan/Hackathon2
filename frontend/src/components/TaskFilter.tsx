// src/components/TaskFilter.tsx
import { useState } from 'react';

interface TaskFilterProps {
  onFilterChange: (filter: 'all' | 'pending' | 'completed') => void;
}

export const TaskFilter = ({ onFilterChange }: TaskFilterProps) => {
  const [activeFilter, setActiveFilter] = useState<'all' | 'pending' | 'completed'>('all');

  const handleFilterClick = (filter: 'all' | 'pending' | 'completed') => {
    setActiveFilter(filter);
    onFilterChange(filter);
  };

  return (
    <div className="flex space-x-2 mb-4">
      <button
        onClick={() => handleFilterClick('all')}
        className={`px-4 py-2 rounded-md text-sm font-medium ${
          activeFilter === 'all'
            ? 'bg-indigo-600 text-white'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }`}
      >
        All
      </button>
      <button
        onClick={() => handleFilterClick('pending')}
        className={`px-4 py-2 rounded-md text-sm font-medium ${
          activeFilter === 'pending'
            ? 'bg-indigo-600 text-white'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }`}
      >
        Pending
      </button>
      <button
        onClick={() => handleFilterClick('completed')}
        className={`px-4 py-2 rounded-md text-sm font-medium ${
          activeFilter === 'completed'
            ? 'bg-indigo-600 text-white'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }`}
      >
        Completed
      </button>
    </div>
  );
};