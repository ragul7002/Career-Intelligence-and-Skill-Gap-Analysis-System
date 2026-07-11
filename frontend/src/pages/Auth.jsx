import React, { useState } from 'react';
import { Lock, Mail, User, BookOpen, GraduationCap, Calendar, Sparkles } from 'lucide-react';
import { API_URL } from '../App';

function Auth({ onAuthSuccess, onNavigate }) {
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Form states
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [college, setCollege] = useState('');
  const [degree, setDegree] = useState('');
  const [gradYear, setGradYear] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const endpoint = isLogin ? '/login' : '/register';
    const payload = isLogin 
      ? { email, password } 
      : { name, email, password, college, degree, graduation_year: parseInt(gradYear) || 2026 };

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Something went wrong!');
      }

      // Success
      onAuthSuccess(data.token, data.user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-grow flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-slate-50 dark:bg-slate-950 relative overflow-hidden bg-gradient-mesh">
      {/* Glow Effects - Now Floating */}
      <div className="absolute top-1/4 left-1/4 w-[400px] h-[400px] bg-primary-500/10 dark:bg-primary-500/5 rounded-full blur-3xl pointer-events-none animate-float-slow"></div>
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-secondary-500/10 dark:bg-secondary-500/5 rounded-full blur-3xl pointer-events-none animate-float"></div>

      <div className="max-w-md w-full space-y-8 glass-panel p-8 rounded-3xl relative z-10 border border-slate-200/50 dark:border-slate-800/40 animate-fade-in-up">
        
        {/* Header */}
        <div className="text-center">
          <div className="mx-auto h-12 w-12 rounded-2xl bg-gradient-to-tr from-primary-500 to-secondary-500 flex items-center justify-center text-white shadow-lg shadow-primary-500/20">
            <Sparkles className="h-6 w-6" />
          </div>
          <h2 className="mt-6 text-3xl font-extrabold text-slate-900 dark:text-white">
            {isLogin ? 'Welcome Back' : 'Create Your Account'}
          </h2>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
            {isLogin ? 'Access your resume reports and skill tracking' : 'Analyze your skills against top technology standards'}
          </p>
        </div>

        {/* Tab Selection */}
        <div className="flex border-b border-slate-200 dark:border-slate-800">
          <button
            onClick={() => { setIsLogin(true); setError(''); }}
            className={`w-1/2 pb-3 text-xs font-bold transition-all border-b-2 ${
              isLogin 
                ? 'border-primary-500 text-primary-600 dark:text-primary-400' 
                : 'border-transparent text-slate-400 hover:text-slate-600 dark:hover:text-slate-200'
            }`}
          >
            Sign In
          </button>
          <button
            onClick={() => { setIsLogin(false); setError(''); }}
            className={`w-1/2 pb-3 text-xs font-bold transition-all border-b-2 ${
              !isLogin 
                ? 'border-primary-500 text-primary-600 dark:text-primary-400' 
                : 'border-transparent text-slate-400 hover:text-slate-600 dark:hover:text-slate-200'
            }`}
          >
            Register
          </button>
        </div>

        {/* Errors */}
        {error && (
          <div className="p-3.5 bg-red-500/10 border border-red-500/25 text-red-600 dark:text-red-400 rounded-xl text-xs font-medium">
            {error}
          </div>
        )}

        {/* Form */}
        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          
          {/* Register-only inputs */}
          {!isLogin && (
            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Full Name</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <User className="h-4 w-4" />
                </div>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="block w-full pl-10 pr-3 py-3 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 rounded-xl text-xs focus:outline-none focus:border-primary-500 transition-colors"
                  placeholder="John Doe"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Email Address</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                <Mail className="h-4 w-4" />
              </div>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="block w-full pl-10 pr-3 py-3 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 rounded-xl text-xs focus:outline-none focus:border-primary-500 transition-colors"
                placeholder="name@college.edu"
              />
            </div>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Password</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                <Lock className="h-4 w-4" />
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="block w-full pl-10 pr-3 py-3 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 rounded-xl text-xs focus:outline-none focus:border-primary-500 transition-colors"
                placeholder="••••••••"
              />
            </div>
          </div>

          {/* Register-only college metadata */}
          {!isLogin && (
            <div className="space-y-4 pt-2 border-t border-slate-100 dark:border-slate-900">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">College</label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                      <BookOpen className="h-3.5 w-3.5" />
                    </div>
                    <input
                      type="text"
                      required
                      value={college}
                      onChange={(e) => setCollege(e.target.value)}
                      className="block w-full pl-9 pr-3 py-2.5 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 rounded-xl text-xs focus:outline-none focus:border-primary-500"
                      placeholder="University Name"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Degree</label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                      <GraduationCap className="h-3.5 w-3.5" />
                    </div>
                    <input
                      type="text"
                      required
                      value={degree}
                      onChange={(e) => setDegree(e.target.value)}
                      className="block w-full pl-9 pr-3 py-2.5 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 rounded-xl text-xs focus:outline-none focus:border-primary-500"
                      placeholder="B.S. Comp Sci"
                    />
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Graduation Year</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                    <Calendar className="h-3.5 w-3.5" />
                  </div>
                  <input
                    type="number"
                    required
                    min="2020"
                    max="2035"
                    value={gradYear}
                    onChange={(e) => setGradYear(e.target.value)}
                    className="block w-full pl-9 pr-3 py-2.5 border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 rounded-xl text-xs focus:outline-none focus:border-primary-500"
                    placeholder="2026"
                  />
                </div>
              </div>
            </div>
          )}

          {isLogin && (
            <div className="flex items-center justify-between text-[11px] text-slate-500">
              <label className="flex items-center space-x-1.5 cursor-pointer">
                <input type="checkbox" className="rounded text-primary-600 focus:ring-primary-500" />
                <span>Remember Me</span>
              </label>
              <a href="#" onClick={(e) => { e.preventDefault(); alert("Feature coming soon! Direct database password reset is not supported yet."); }} className="font-semibold text-primary-500 hover:text-primary-600">
                Forgot Password?
              </a>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-6 py-3 px-4 rounded-xl bg-gradient-to-r from-primary-600 to-secondary-600 text-white font-bold text-xs hover:from-primary-700 hover:to-secondary-700 active:scale-98 transition-all shadow-md shadow-primary-500/10 disabled:opacity-50"
          >
            {loading ? 'Processing...' : isLogin ? 'Sign In' : 'Create Account'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Auth;
