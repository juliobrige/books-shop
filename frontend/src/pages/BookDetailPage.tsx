// src/pages/BookDetailPage.tsx
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../api/apiClient';

// A nossa interface para um único livro
interface Book {
  id: number;
  title: string;
  description: string;
  authors: { name: string }[];
  price: string;
  cover: string;
}

function BookDetailPage() {
  const { bookId } = useParams<{ bookId: string }>(); // Pega o ID do livro a partir do URL
  const [book, setBook] = useState<Book | null>(null);

  useEffect(() => {
    if (bookId) {
      apiClient.get(`/store/books/${bookId}/`)
        .then(response => {
          setBook(response.data);
        })
        .catch(error => console.error("Erro ao buscar detalhes do livro:", error));
    }
  }, [bookId]); // Executa sempre que o bookId mudar

  if (!book) {
    return <div className="text-center text-white p-8">A carregar...</div>;
  }

  return (
    <div className="bg-gray-900 text-white min-h-screen p-8">
      <div className="container mx-auto">
        <h1 className="text-4xl font-bold mb-4">{book.title}</h1>
        <p className="text-xl text-gray-400 mb-6">por {book.authors.map(a => a.name).join(', ')}</p>
        <p className="text-gray-300">{book.description}</p>
        <p className="text-3xl font-bold mt-8 text-blue-400">{book.price} €</p>
      </div>
    </div>
  );
}

export default BookDetailPage;