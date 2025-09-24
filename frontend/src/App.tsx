// src/App.tsx
import { Outlet } from 'react-router-dom';
import Navbar from './components/Navbar'; // Importe a Navbar

function App() {
  return (
    <div>
      <Navbar /> {/* Adicione a Navbar aqui */}
      <main>
        <Outlet />
      </main>
    </div>
  );
}

export default App;