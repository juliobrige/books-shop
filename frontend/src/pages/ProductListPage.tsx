// src/pages/ProductListPage.tsx
import { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';
import BookCard from '../components/BookCard';
import CategoryFilter from '../components/CategoryFilter';

// Interfaces para os nossos dados
interface PaginatedResponse<T> {
  results: T[];
}
interface Book {
  id: number;
  title: string;
  authors: { name: string }[];
  price: string;
  cover_image: string | null;
}

function ProductListPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState(''); // Estado para o filtro de categoria
  const [ordering, setOrdering] = useState(''); // Estado para a ordenação

  useEffect(() => {
    setLoading(true);
    
    // Constrói os parâmetros da query para a API
    const params = new URLSearchParams();
    if (category) {
      params.append('category__slug', category);
    }
    if (ordering) {
      params.append('ordering', ordering);
    }

    // Faz o pedido à API com os filtros e ordenação
    apiClient.get<PaginatedResponse<Book>>(`/store/books/?${params.toString()}`)
      .then(response => {
        setBooks(response.data.results);
      })
      .catch(error => {
        console.error("Erro ao buscar a lista de livros:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [category, ordering]); // Re-executa quando a categoria ou a ordenação mudam

  return (
    <section className="bg-gray-50 py-8 antialiased dark:bg-gray-900 md:py-12">
      <div className="mx-auto max-w-screen-xl px-4 2xl:px-0">
        
        {/* Cabeçalho e Botão de Ordenação do Novo Template */}
        <div className="mb-4 items-end justify-between space-y-4 sm:flex sm:space-y-0 md:mb-8">
          <div>
            <h2 className="mt-3 text-xl font-semibold text-gray-900 dark:text-white sm:text-2xl">Nosso Catálogo</h2>
          </div>
          <div className="flex items-center space-x-4">
            {/* Dropdown de Ordenação (Lógica a ser adicionada) */}
            <select 
              onChange={(e) => setOrdering(e.target.value)} 
              value={ordering}
              className="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-900 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400"
            >
              <option value="">Ordenar por</option>
              <option value="title">Título (A-Z)</option>
              <option value="-title">Título (Z-A)</option>
              <option value="price">Preço (Crescente)</option>
              <option value="-price">Preço (Decrescente)</option>
            </select>
          </div>
        </div>

        {/* Layout de 2 Colunas com a Lógica de Filtro */}
        <div className="md:flex md:gap-8">
          
          {/* Coluna de Filtros (Esquerda) com nosso componente funcional */}
          <aside className="w-full md:w-1/4 lg:w-1/5 mb-8 md:mb-0">
            <CategoryFilter 
              selectedCategory={category}
              onCategoryChange={setCategory}
            />
          </aside>

          {/* Coluna de Conteúdo (Direita) */}
          <main className="w-full md:w-3/4 lg:w-4/5">
            {loading ? (
              <p className="text-white text-center">A carregar livros...</p>
            ) : (
              <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3">
                {books.length > 0 ? books.map(book => (
                  <BookCard key={book.id} book={book} />
                )) : (
                  <p className="text-gray-400 col-span-full text-center">Nenhum livro encontrado para esta seleção.</p>
                )}
              </div>
            )}
            
            {/* Botão "Mostrar mais" (ainda estático) */}
            <div className="w-full text-center mt-8">
              <button type="button" className="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-900 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400">
                Mostrar mais
              </button>
            </div>
          </main>

        </div>
      </div>
    </section>
  );
}

export default ProductListPage;