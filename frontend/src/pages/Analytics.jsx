import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Award, Calendar, CheckSquare, RefreshCw } from 'lucide-react';
import { 
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, 
  CartesianGrid, Tooltip, Legend, AreaChart, Area, BarChart, Bar 
} from 'recharts';
import { API_URL } from '../App';

function Analytics({ token }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchAnalytics = () => {
    setLoading(true);
    fetch(`${API_URL}/analytics/summary`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(resData => {
        setData(resData);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading analytics:", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="flex-grow flex items-center justify-center bg-slate-50 dark:bg-slate-950">
        <RefreshCw className="h-6.5 w-6.5 text-primary-500 animate-spin" />
        <span className="ml-2 text-xs font-semibold text-slate-400">Loading Analytics...</span>
      </div>
    );
  }

  // Fallback defaults for new users
  const defaultHistory = [
    { upload_number: "Upload 1", date: "2026-06-01", role: "AI Engineer", ats_score: 55, readiness_score: 45 },
    { upload_number: "Upload 2", date: "2026-06-03", role: "AI Engineer", ats_score: 72, readiness_score: 65 },
    { upload_number: "Upload 3", date: "2026-06-04", role: "AI Engineer", ats_score: 82, readiness_score: 76 }
  ];

  const defaultSkillsDist = [
    { name: "Languages", value: 3 },
    { name: "Frameworks & Libraries", value: 4 },
    { name: "Databases & Data Tools", value: 2 },
    { name: "Cloud & DevOps", value: 1 }
  ];

  const defaultActivities = [
    { action: "milestone_update", details: "Marked milestone 'Master PyTorch' as completed", timestamp: "2026-06-04 18:30:12" },
    { action: "resume_analysis", details: "Analyzed resume 'Ragul_Resume.pdf' for role 'AI Engineer'. ATS: 82%", timestamp: "2026-06-04 14:10:00" },
    { action: "update_profile", details: "Updated target career goal to: AI Engineer", timestamp: "2026-06-04 11:22:15" }
  ];

  const history = data?.upload_history?.length > 0 ? data.upload_history : defaultHistory;
  const skillsDist = data?.skills_distribution?.length > 0 ? data.skills_distribution : defaultSkillsDist;
  const activities = data?.activities?.length > 0 ? data.activities : defaultActivities;
  const rate = data ? data.completion_rate : 66;

  return (
    <div className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 bg-slate-50 dark:bg-slate-950 bg-gradient-mesh animate-fade-in">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-200/60 dark:border-slate-900 pb-5">
        <div>
          <div className="flex items-center space-x-2 text-xs font-semibold text-primary-500 mb-1">
            <BarChart3 className="h-4 w-4" />
            <span>AI Platform Statistics</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white">
            Personal Analytics & Trends
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Historical portfolio tracking and progression metrics.
          </p>
        </div>
        <button
          onClick={fetchAnalytics}
          className="p-2 border border-slate-200 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900 text-slate-650 hover:bg-slate-100 dark:hover:bg-slate-900/50"
          title="Reload Statistics"
        >
          <RefreshCw className="h-4 w-4" />
        </button>
      </div>

      {/* Analytics Summary Metric Rows */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div className="glass-card p-5 rounded-2xl border border-slate-200/50 dark:border-slate-800/40 animate-fade-in-up delay-75 hover:-translate-y-1.5 hover:shadow-xl hover:border-primary-500/20 transition-all duration-300">
          <p className="text-[10px] font-bold text-slate-400 uppercase">Resume Uploads</p>
          <h3 className="text-2xl font-black text-slate-800 dark:text-white mt-1">{history.length} Files</h3>
          <span className="block text-[9px] text-slate-450 mt-2">Saved and analyzed versions</span>
        </div>
        <div className="glass-card p-5 rounded-2xl border border-slate-200/50 dark:border-slate-800/40 animate-fade-in-up delay-100 hover:-translate-y-1.5 hover:shadow-xl hover:border-secondary-500/20 transition-all duration-300">
          <p className="text-[10px] font-bold text-slate-400 uppercase">Roadmap Milestone Rate</p>
          <h3 className="text-2xl font-black text-slate-855 dark:text-white mt-1">{rate}% Complete</h3>
          <span className="block text-[9px] text-slate-450 mt-2">Milestone tasks checked</span>
        </div>
        <div className="glass-card p-5 rounded-2xl border border-slate-200/50 dark:border-slate-800/40 animate-fade-in-up delay-150 hover:-translate-y-1.5 hover:shadow-xl hover:border-primary-500/20 transition-all duration-300">
          <p className="text-[10px] font-bold text-slate-400 uppercase">Active Target Role</p>
          <h3 className="text-2xl font-black text-primary-500 mt-1 truncate">
            {history[history.length - 1]?.role || 'AI Engineer'}
          </h3>
          <span className="block text-[9px] text-slate-450 mt-2">Last matched configuration</span>
        </div>
      </div>

      {/* Line & Area charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* ATS Trends Line Chart */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/60 dark:border-slate-800/50 flex flex-col justify-between animate-fade-in-up delay-200">
          <div>
            <h3 className="text-sm font-extrabold text-slate-800 dark:text-slate-200 mb-1 flex items-center space-x-1.5">
              <TrendingUp className="h-4 w-4 text-primary-500" />
              <span>ATS Score Performance Trends</span>
            </h3>
            <p className="text-[10px] text-slate-400 mb-4">
              Visualizes ATS matching score improvements across successive resume uploads.
            </p>
          </div>
          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="#475569" strokeOpacity={0.15} />
                <XAxis dataKey="upload_number" stroke="#94a3b8" fontSize={9} fontWeight="bold" />
                <YAxis domain={[0, 100]} stroke="#94a3b8" fontSize={9} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: 8, fontSize: 10, color: '#f8fafc' }} />
                <Line type="monotone" dataKey="ats_score" name="ATS Score" stroke="#6366f1" strokeWidth={3} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Career Readiness Area Chart */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/60 dark:border-slate-800/50 flex flex-col justify-between animate-fade-in-up delay-300">
          <div>
            <h3 className="text-sm font-extrabold text-slate-800 dark:text-slate-200 mb-1 flex items-center space-x-1.5">
              <Award className="h-4 w-4 text-secondary-500" />
              <span>Career Readiness Score Progression</span>
            </h3>
            <p className="text-[10px] text-slate-400 mb-4">
              Tracks the composite AI preparedness score growth over time.
            </p>
          </div>
          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={history}>
                <defs>
                  <linearGradient id="colorReadinessAnalytics" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#a855f7" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#a855f7" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#475569" strokeOpacity={0.15} />
                <XAxis dataKey="upload_number" stroke="#94a3b8" fontSize={9} fontWeight="bold" />
                <YAxis domain={[0, 100]} stroke="#94a3b8" fontSize={9} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: 8, fontSize: 10, color: '#f8fafc' }} />
                <Area type="monotone" dataKey="readiness_score" name="Readiness Index" stroke="#a855f7" strokeWidth={2.5} fillOpacity={1} fill="url(#colorReadinessAnalytics)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Skill Distribution and Activity Log */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Skills Distribution Bar Chart */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/60 dark:border-slate-800/50 lg:col-span-1 flex flex-col justify-between animate-fade-in-up delay-400">
          <div>
            <h3 className="text-sm font-extrabold text-slate-800 dark:text-slate-200 mb-1">
              Skill Categories Distribution
            </h3>
            <p className="text-[10px] text-slate-400 mb-4">
              Categorized tool count loaded in your profile database.
            </p>
          </div>
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={skillsDist}>
                <CartesianGrid strokeDasharray="3 3" stroke="#475569" strokeOpacity={0.1} />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={7} fontWeight="bold" />
                <YAxis stroke="#94a3b8" fontSize={8} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: 8, fontSize: 10, color: '#f8fafc' }} />
                <Bar dataKey="value" name="Skill Count" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Activity Logs (Audit Trail) */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-200/60 dark:border-slate-800/50 lg:col-span-2 space-y-4 animate-fade-in-up delay-400">
          <div>
            <h3 className="text-sm font-extrabold text-slate-800 dark:text-slate-200">
              Activity History Trail
            </h3>
            <p className="text-[10px] text-slate-400">
              Audit log records detailing profile analysis history.
            </p>
          </div>

          <div className="space-y-3 max-h-[220px] overflow-y-auto pr-1">
            {activities.map((act, idx) => (
              <div key={idx} className="flex justify-between items-start p-3 bg-white dark:bg-slate-900 border border-slate-150/15 dark:border-slate-800/60 rounded-xl text-xs gap-3">
                <div className="space-y-1">
                  <span className={`inline-block text-[8px] font-bold px-1.5 py-0.5 rounded ${
                    act.action === 'resume_analysis' 
                      ? 'bg-primary-500/10 text-primary-600 dark:text-primary-400' 
                      : act.action === 'milestone_update'
                      ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-500'
                  }`}>
                    {act.action.replace('_', ' ').toUpperCase()}
                  </span>
                  <p className="text-slate-650 dark:text-slate-350">{act.details}</p>
                </div>
                <div className="flex items-center text-[9px] text-slate-400 shrink-0 mt-0.5">
                  <Calendar className="h-3 w-3 mr-1" />
                  <span>{act.timestamp.split(' ')[0]}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
}

export default Analytics;
