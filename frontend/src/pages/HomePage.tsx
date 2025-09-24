// src/pages/HomePage.tsx

import { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';
import BookCard from '../components/BookCard';

// Interface corrigida para incluir a imagem da capa
interface Book {
  id: number;
  title: string;
  authors: { name: string }[];
  price: string;
  cover_image: string | null; // <-- Campo adicionado
}

function HomePage() {
  const [books, setBooks] = useState<Book[]>([]);

  useEffect(() => {
    apiClient.get('/store/books/') 
      .then(response => {
        // Assumindo que a sua API é paginada
        setBooks(response.data.results);
      })
      .catch(error => {
        console.error("Houve um erro ao buscar os livros!", error);
      });
  }, []);

  return (
    <div className="bg-gray-900 min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-8 text-center text-white">Catálogo de Livros</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {books.map(book => (
          // CORREÇÃO: A prop agora chama-se 'book'
          <BookCard key={book.id} book={book} />
        ))}
      </div>
    </div>
  );
}

export default HomePage;