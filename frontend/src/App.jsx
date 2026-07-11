import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import Auth from './pages/Auth';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import AdminPanel from './pages/AdminPanel';

export const API_URL = window.location.port === '5173'
  ? `http://${window.location.hostname}:5000/api`
  : `${window.location.origin}/api`;

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')) || null);
  const [currentPage, setCurrentPage] = useState('landing'); // landing, auth, dashboard, analytics, admin
  const [darkMode, setDarkMode] = useState(true);

  // Apply dark mode class to HTML element
  useEffect(() => {
    const root = window.document.documentElement;
    if (darkMode) {
      root.classList.add('dark');
      root.classList.remove('light');
    } else {
      root.classList.add('light');
      root.classList.remove('dark');
    }
  }, [darkMode]);

  // Sync token to localStorage
  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  // Sync user details to localStorage
  useEffect(() => {
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
    } else {
      localStorage.removeItem('user');
    }
  }, [user]);

  // On load, verify profile and redirect to dashboard if authenticated
  useEffect(() => {
    if (token) {
      fetch(`${API_URL}/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then(res => {
        if (res.status === 401) {
          // Token expired or invalid
          setToken('');
          setUser(null);
          setCurrentPage('auth');
        } else if (res.ok) {
          return res.json();
        }
      })
      .then(data => {
        if (data) {
          setUser(data.user);
          if (currentPage === 'landing' || currentPage === 'auth') {
            setCurrentPage('dashboard');
          }
        }
      })
      .catch(err => {
        console.error("Profile check failed:", err);
      });
    }
  }, [token]);

  const handleLogout = () => {
    setToken('');
    setUser(null);
    setCurrentPage('landing');
  };

  const handleLoginSuccess = (newToken, newUser) => {
    setToken(newToken);
    setUser(newUser);
    setCurrentPage('dashboard');
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'landing':
        return <LandingPage onNavigate={setCurrentPage} token={token} />;
      case 'auth':
        return <Auth onAuthSuccess={handleLoginSuccess} onNavigate={setCurrentPage} />;
      case 'dashboard':
        return token ? <Dashboard token={token} user={user} /> : <Auth onAuthSuccess={handleLoginSuccess} onNavigate={setCurrentPage} />;
      case 'analytics':
        return token ? <Analytics token={token} /> : <Auth onAuthSuccess={handleLoginSuccess} onNavigate={setCurrentPage} />;
      case 'admin':
        return token && user?.role === 'admin' ? <AdminPanel token={token} /> : <Dashboard token={token} user={user} />;
      default:
        return <LandingPage onNavigate={setCurrentPage} token={token} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-950 dark:text-slate-50 flex flex-col transition-colors duration-300">
      <Navbar 
        currentPage={currentPage} 
        setCurrentPage={setCurrentPage} 
        user={user} 
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        onLogout={handleLogout}
      />
      <main key={currentPage} className="flex-grow flex flex-col animate-fade-in">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
