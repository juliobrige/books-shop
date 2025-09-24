// src/components/Navbar.tsx

import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // <-- CORREÇÃO: Usamos ../ para subir um nível

function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-gray-800 p-4 shadow-lg text-white">
      <div className="container mx-auto flex justify-between items-center">
        {/* Lado Esquerdo */}
        <div className="flex items-center space-x-8">
          <Link to="/" className="text-2xl font-bold hover:text-blue-400">
            Books-Shop
          </Link>
          <div className="hidden md:flex items-center space-x-4">
            <Link to="/" className="hover:text-blue-400">Livros</Link>
            {/* Adicione um link para cursos quando a página existir */}
            {/* <Link to="/courses" className="hover:text-blue-400">Cursos</Link> */}
          </div>
        </div>

        {/* Lado Direito */}
        <div className="flex items-center space-x-4">
          {user ? (
            // Se o utilizador estiver autenticado
            <>
              <span>Olá, {user.username}!</span>
              <button onClick={logout} className="bg-red-600 hover:bg-red-700 px-3 py-2 rounded">
                Sair
              </button>
            </>
          ) : (
            // Se o utilizador NÃO estiver autenticado
            <>
              <Link to="/login" className="hover:text-blue-400">Login</Link>
              <Link to="/register" className="bg-blue-600 hover:bg-blue-700 px-3 py-2 rounded">
                Registar
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;