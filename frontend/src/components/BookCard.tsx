// src/components/BookCard.tsx
import { Link } from 'react-router-dom';

interface Author {
  name: string;
}

interface Book {
  id: number;
  title: string;
  authors: Author[];
  price: string;
  cover_image: string | null; // A imagem pode ser nula
}

interface BookCardProps {
  book: Book;
}

function BookCard({ book }: BookCardProps) {
  const authorName = book.authors && book.authors.length > 0
    ? book.authors[0].name
    : 'Autor Desconhecido';

  return (
    <Link to={`/books/${book.id}`} className="block h-full">
      <div className="bg-gray-800 rounded-lg p-4 flex flex-col shadow-lg hover:scale-105 transition-transform duration-200 h-full">
        
        {/* CÓDIGO DA IMAGEM ADICIONADO AQUI */}
        <div className="h-56 w-full mb-4">
          {book.cover_image ? (
            <img 
              src={book.cover_image} 
              alt={`Capa do livro ${book.title}`} 
              className="w-full h-full object-contain" 
            />
          ) : (
            <div className="w-full h-full bg-gray-700 flex items-center justify-center rounded">
              <span className="text-gray-500">Sem Capa</span>
            </div>
          )}
        </div>
        
        <h2 className="text-xl font-semibold mb-2 text-white">{book.title}</h2>
        <p className="text-gray-400 mb-4">por {authorName}</p>
        <p className="text-2xl font-bold mt-auto text-blue-400">{book.price} €</p>
      </div>
    </Link>
  );
}

export default BookCard;