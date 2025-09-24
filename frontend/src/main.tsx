// src/main.tsx

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// 1. Importações do Router
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext'; // 1. Importe o provider

// 2. Importamos as nossas páginas
import HomePage from './pages/HomePage.tsx';
import BookDetailPage from './pages/BookDetailPage.tsx';
import LoginPage from './pages/LoginPage.tsx';
import ProductListPage from './pages/ProductListPage.tsx';


// 3. Definimos as nossas rotas
const router = createBrowserRouter([
  {
    path: "/",
    element: <App />, // O <App /> é o layout principal
    children: [
      {
        path: "/",
        element: <HomePage />, // A página inicial
      },
      {
        path: "/books/:bookId", // Rota para os detalhes de um livro (agora ativa)
        element: <BookDetailPage />,
      },
        { path: "/", element: <ProductListPage /> }, // Nova página principal

      { path: "/login", element: <LoginPage /> }
    ]
  }
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AuthProvider> {/* 2. Adicione o AuthProvider aqui */}
      <RouterProvider router={router} />
    </AuthProvider>
  </React.StrictMode>,
)