// src/pages/LoginPage.tsx
import { useState } from 'react';
// CORREÇÃO: Adicionado useNavigate
import { useNavigate } from 'react-router-dom'; 
import apiClient from '../api/apiClient';
// CORREÇÃO: Caminho corrigido com ../
import { useAuth } from '../context/AuthContext'; 

// ... resto do seu componente ...
function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

const { login } = useAuth(); // Use o nosso contexto
const navigate = useNavigate(); // Para redirecionar o utilizador

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');

    try {
      const response = await apiClient.post('/api/token/', {
        username,
        password,
      });
      login(response.data); // Usa a função de login do contexto
      navigate('/'); // Redireciona para a página inicial
    } catch (err) {
      setError('Nome de utilizador ou senha inválidos.');
    }
  };

  return (
    // Div principal que centra o formulário no ecrã
    <div className="bg-gray-900 min-h-screen flex items-center justify-center">
      
      {/* O cartão do formulário */}
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-2xl font-bold text-white mb-6 text-center">Login</h2>
        
        <form onSubmit={handleSubmit}>
          {/* Campo Username */}
          <div className="mb-4">
            <label className="block text-gray-400 mb-2" htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full p-3 rounded bg-gray-700 text-white border border-gray-600 focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* Campo Password */}
          <div className="mb-6">
            <label className="block text-gray-400 mb-2" htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-3 rounded bg-gray-700 text-white border border-gray-600 focus:outline-none focus:border-blue-500"
            />
          </div>
          
          {/* Mensagem de Erro */}
          {error && <p className="text-red-500 text-center mb-4">{error}</p>}
          
          {/* Botão de Submissão */}
          <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded transition duration-300">
            Entrar
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;