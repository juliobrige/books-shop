// src/context/AuthContext.tsx
import { createContext, useState, useContext, useEffect } from 'react';
import type { ReactNode } from 'react';
import { jwtDecode } from 'jwt-decode';import apiClient from '../api/apiClient';

// Tipos
interface AuthToken {
  access: string;
  refresh: string;
}
interface JwtPayload {
  user_id: number;
  username: string;
  exp: number;
  iat: number;
}
interface User {
  user_id: number;
  username: string;
}
interface AuthContextType {
  user: User | null;
  login: (tokens: AuthToken) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const tokens = localStorage.getItem('authTokens');
    if (tokens) {
      const parsedTokens: AuthToken = JSON.parse(tokens);
      const decodedUser = jwtDecode<JwtPayload>(parsedTokens.access);
      const now = Date.now() / 1000;

      if (decodedUser.exp > now) {
        setUser({ user_id: decodedUser.user_id, username: decodedUser.username });
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${parsedTokens.access}`;
      } else {
        localStorage.removeItem('authTokens');
      }
    }
  }, []);

  const login = (tokens: AuthToken) => {
    localStorage.setItem('authTokens', JSON.stringify(tokens));
    const decodedUser = jwtDecode<JwtPayload>(tokens.access);
    setUser({ user_id: decodedUser.user_id, username: decodedUser.username });
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${tokens.access}`;
  };

  const logout = () => {
    localStorage.removeItem('authTokens');
    setUser(null);
    delete apiClient.defaults.headers.common['Authorization'];
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook personalizado
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
