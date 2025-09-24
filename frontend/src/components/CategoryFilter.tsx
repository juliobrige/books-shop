// src/components/CategoryFilter.tsx
import { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';

interface Category {
  id: number;
  name: string;
  slug: string;
}

interface CategoryFilterProps {
  selectedCategory: string;
  onCategoryChange: (slug: string) => void;
}

function CategoryFilter({ selectedCategory, onCategoryChange }: CategoryFilterProps) {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    apiClient.get('/store/categories/')
      .then(response => {
        setCategories(response.data.results);
      })
      .catch(error => console.error("Erro ao buscar categorias:", error));
  }, []);

  return (
    <div>
      <h3 className="text-lg font-semibold text-white mb-2">Categorias</h3>
      <ul className="space-y-1">
        <li>
          <button
            onClick={() => onCategoryChange('')}
            className={`w-full text-left p-2 rounded ${selectedCategory === '' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:bg-gray-700'}`}
          >
            Todas
          </button>
        </li>
        {categories.map(category => (
          <li key={category.id}>
            <button
              onClick={() => onCategoryChange(category.slug)}
              className={`w-full text-left p-2 rounded ${selectedCategory === category.slug ? 'bg-blue-600 text-white' : 'text-gray-400 hover:bg-gray-700'}`}
            >
              {category.name}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CategoryFilter;