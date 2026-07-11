import React, { useState } from 'react';
import { Sun, Moon, LogOut, LayoutDashboard, BarChart3, ShieldAlert, Sparkles, User } from 'lucide-react';

function Navbar({ currentPage, setCurrentPage, user, darkMode, setDarkMode, onLogout }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-white/70 dark:bg-slate-900/60 backdrop-blur-md border-b border-slate-200/50 dark:border-slate-800/40 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div 
            className="flex items-center space-x-2 cursor-pointer group"
            onClick={() => setCurrentPage('landing')}
          >
            <div className="p-2 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg text-white shadow-md shadow-primary-500/20 group-hover:scale-105 transition-transform">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-primary-600 via-primary-500 to-secondary-500 dark:from-primary-400 dark:via-primary-300 dark:to-secondary-400 bg-clip-text text-transparent">
                AI Skill Accelerator
              </span>
              <span className="block text-[10px] text-slate-400 font-medium tracking-wider -mt-1 uppercase">
                Accelerate Career Growth
              </span>
            </div>
          </div>

          {/* Navigation Links */}
          {user && (
            <div className="hidden md:flex items-center space-x-1">
              <button
                onClick={() => setCurrentPage('dashboard')}
                className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  currentPage === 'dashboard'
                    ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400'
                    : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/50'
                }`}
              >
                <LayoutDashboard className="h-4 w-4" />
                <span>Dashboard</span>
              </button>

              <button
                onClick={() => setCurrentPage('analytics')}
                className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  currentPage === 'analytics'
                    ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400'
                    : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/50'
                }`}
              >
                <BarChart3 className="h-4 w-4" />
                <span>Analytics</span>
              </button>

              {user.role === 'admin' && (
                <button
                  onClick={() => setCurrentPage('admin')}
                  className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    currentPage === 'admin'
                      ? 'bg-red-500/10 text-red-600 dark:text-red-400'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/50'
                  }`}
                >
                  <ShieldAlert className="h-4 w-4" />
                  <span>Admin Panel</span>
                </button>
              )}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex items-center space-x-3">
            {/* Dark Mode Toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/50 border border-slate-200/40 dark:border-slate-800/40 transition-colors"
              aria-label="Toggle Theme"
            >
              {darkMode ? <Sun className="h-4 w-4 text-amber-400" /> : <Moon className="h-4 w-4" />}
            </button>

            {user ? (
              <div className="relative">
                <button
                  onClick={() => setIsOpen(!isOpen)}
                  className="flex items-center space-x-2 p-1.5 rounded-lg border border-slate-200/40 dark:border-slate-800/40 bg-slate-50 dark:bg-slate-900/40 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all"
                >
                  <div className="h-7 w-7 rounded-full bg-gradient-to-tr from-primary-500 to-secondary-500 flex items-center justify-center text-white text-xs font-bold shadow-sm">
                    {user.name.charAt(0).toUpperCase()}
                  </div>
                  <span className="hidden sm:inline text-xs font-semibold text-slate-700 dark:text-slate-300">
                    {user.name.split(' ')[0]}
                  </span>
                </button>

                {isOpen && (
                  <div className="absolute right-0 mt-2 w-48 rounded-xl border border-slate-200/60 dark:border-slate-800/50 bg-white dark:bg-slate-900 shadow-2xl p-2 z-50">
                    <div className="px-3 py-2 border-b border-slate-100 dark:border-slate-800/60 mb-1">
                      <p className="text-xs font-semibold text-slate-800 dark:text-slate-200 truncate">{user.name}</p>
                      <p className="text-[10px] text-slate-400 truncate">{user.email}</p>
                    </div>
                    
                    <button
                      onClick={() => {
                        setIsOpen(false);
                        setCurrentPage('dashboard');
                      }}
                      className="w-full flex items-center space-x-2 px-3 py-2 text-left text-xs rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/50 transition-colors"
                    >
                      <User className="h-3.5 w-3.5" />
                      <span>My Profile</span>
                    </button>
                    
                    <button
                      onClick={() => {
                        setIsOpen(false);
                        onLogout();
                      }}
                      className="w-full flex items-center space-x-2 px-3 py-2 text-left text-xs rounded-lg text-red-600 dark:text-red-400 hover:bg-red-500/10 transition-colors"
                    >
                      <LogOut className="h-3.5 w-3.5" />
                      <span>Sign Out</span>
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <button
                onClick={() => setCurrentPage('auth')}
                className="inline-flex items-center justify-center px-4 py-2 text-xs font-semibold rounded-lg bg-primary-600 dark:bg-primary-500 text-white hover:bg-primary-700 dark:hover:bg-primary-600 shadow-md shadow-primary-500/20 active:scale-95 transition-all"
              >
                Sign In
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
