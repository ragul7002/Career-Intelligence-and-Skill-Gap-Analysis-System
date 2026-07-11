import React, { useState } from 'react';
import { Sparkles, FileSearch, TrendingUp, Compass, Target, ArrowRight, BookOpen, Layers, CheckCircle2, ChevronDown } from 'lucide-react';

function LandingPage({ onNavigate, token }) {
  const [activeFaq, setActiveFaq] = useState(null);

  const features = [
    {
      icon: <FileSearch className="h-6 w-6 text-primary-500" />,
      title: "ATS Analysis",
      desc: "Simulate candidate tracking parses. Check formatting, keyword concentrations, section integrity, and parsing capability."
    },
    {
      icon: <Layers className="h-6 w-6 text-secondary-500" />,
      title: "Skill Gap Detection",
      desc: "Instantly cross-reference your skills against professional tech roles to extract exact gaps and strengths."
    },
    {
      icon: <Target className="h-6 w-6 text-emerald-500" />,
      title: "Career Readiness Score",
      desc: "A composite AI-driven readiness score showing how close you are to landing your target job role."
    },
    {
      icon: <Compass className="h-6 w-6 text-amber-500" />,
      title: "Learning Roadmap",
      desc: "Receive a personalized chronological timeline with exact milestone steps and project prompts to learn missing tech."
    },
    {
      icon: <TrendingUp className="h-6 w-6 text-purple-500" />,
      title: "Future Growth Simulator",
      desc: "The ultimate interactive tool. Select skills you plan to learn and instantly simulate your score growth!"
    }
  ];

  const steps = [
    {
      num: "01",
      title: "Create Account",
      desc: "Register with your graduation details, university, and core interests."
    },
    {
      num: "02",
      title: "Select Job Role",
      desc: "Pick from preconfigured roles (AI, ML, DevOps, Web) or paste a custom description."
    },
    {
      num: "03",
      title: "Upload Resume",
      desc: "Upload your PDF resume. Our parsing engine extracts skills and projects."
    },
    {
      num: "04",
      title: "Accelerate Career",
      desc: "Track matching scores, simulate growth, and complete roadmap milestones."
    }
  ];

  const faqs = [
    {
      q: "Is this just an ATS checker?",
      a: "No! Typical ATS checkers only look for formatting errors and simple keywords. The AI Skill Accelerator is a career readiness platform. While we do offer full ATS metrics, our main module extracts skill gaps, simulates how your readiness improves as you learn new skills, and builds a customized chronological study path."
    },
    {
      q: "How does the Future Score Simulator work?",
      a: "This is our primary feature! Under your dashboard, you can see a checklist of skills you are missing. You can toggle checkbox selectors of skills you intend to learn, and our simulator recalculates and projects your upgraded readiness score, estimated study duration, and growth trajectory."
    },
    {
      q: "Can I parse a custom job description?",
      a: "Yes! In addition to our preconfigured roles (AI Engineer, Data Scientist, ML Engineer, DevOps, Full Stack, Data Analyst), you can paste any custom job description. The backend uses scikit-learn cosine similarities to evaluate keyword concentrations and match skills."
    },
    {
      q: "Are my resumes stored securely?",
      a: "Absolutely. All resumes and user files are stored locally in the secure backend upload folder and linked to your private SQL profile."
    }
  ];

  const handleCtaClick = () => {
    if (token) {
      onNavigate('dashboard');
    } else {
      onNavigate('auth');
    }
  };

  return (
    <div className="flex flex-col bg-slate-50 dark:bg-slate-950 transition-colors duration-300 bg-gradient-mesh min-h-screen">
      
      {/* HERO SECTION */}
      <section className="relative pt-24 pb-20 md:pt-32 md:pb-28 overflow-hidden">
        {/* Glow Effects */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-primary-500/10 dark:bg-primary-500/5 rounded-full blur-3xl pointer-events-none animate-float-slow"></div>
        <div className="absolute top-1/3 left-1/3 w-[300px] h-[300px] bg-secondary-500/10 dark:bg-secondary-500/5 rounded-full blur-3xl pointer-events-none animate-float"></div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-primary-500/10 dark:bg-primary-500/15 border border-primary-500/25 dark:border-primary-500/30 text-primary-600 dark:text-primary-400 text-xs font-semibold mb-6 animate-fade-in-down">
            <Sparkles className="h-4.5 w-4.5 animate-pulse-slow" />
            <span>AI-Powered Skill Acceleration Platform</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-[1.15] mb-6 animate-fade-in-up delay-75">
            Transform Your Resume Into <br />
            <span className="bg-gradient-to-r from-primary-600 via-primary-500 to-secondary-500 dark:from-primary-400 dark:via-primary-300 dark:to-secondary-400 bg-clip-text text-transparent shine-text">
              Career Readiness Success
            </span>
          </h1>

          <p className="max-w-2xl mx-auto text-base sm:text-lg text-slate-500 dark:text-slate-400 mb-10 leading-relaxed animate-fade-in-up delay-150">
            Analyze your resume, identify skill gaps against target jobs, simulate career readiness improvements, follow a personalized learning roadmap, and track your growth journey.
          </p>

          <div className="flex flex-col sm:flex-row justify-center items-center gap-4 animate-fade-in-up delay-200">
            <button
              onClick={handleCtaClick}
              className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-4 text-sm font-semibold rounded-xl bg-primary-600 dark:bg-primary-500 text-white hover:bg-primary-700 dark:hover:bg-primary-600 shadow-xl shadow-primary-500/25 dark:shadow-primary-500/15 hover:scale-[1.03] active:scale-95 transition-all group"
            >
              <span>Analyze Resume</span>
              <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </button>

            <button
              onClick={handleCtaClick}
              className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-4 text-sm font-semibold rounded-xl bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-150 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 hover:scale-[1.03] active:scale-95 transition-all"
            >
              Get Started
            </button>
          </div>

          {/* SaaS Mock Dashboard Preview */}
          <div className="mt-16 max-w-5xl mx-auto border border-slate-200/60 dark:border-slate-800/80 rounded-2xl overflow-hidden shadow-2xl bg-white dark:bg-slate-900 glass-panel p-4 animate-fade-in-up delay-300 hover:scale-[1.01] hover:border-primary-500/35 transition-all duration-500">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3 mb-4">
              <div className="flex items-center space-x-2">
                <span className="h-3.5 w-3.5 rounded-full bg-red-400 block animate-pulse"></span>
                <span className="h-3.5 w-3.5 rounded-full bg-yellow-400 block animate-pulse"></span>
                <span className="h-3.5 w-3.5 rounded-full bg-green-400 block animate-pulse"></span>
              </div>
              <span className="text-xs text-slate-400 font-semibold tracking-wider">workspace_dashboard_v1.0</span>
              <div className="w-16"></div>
            </div>
            
            {/* Fake Dashboard Layout */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-left">
              <div className="p-4 bg-slate-50 dark:bg-slate-950/40 border border-slate-100 dark:border-slate-900 rounded-xl">
                <p className="text-[10px] text-slate-400 font-bold uppercase">ATS score</p>
                <h3 className="text-xl font-bold text-slate-800 dark:text-slate-200">82/100</h3>
                <div className="w-full bg-slate-200 dark:bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                  <div className="bg-primary-500 h-full w-[82%]"></div>
                </div>
              </div>
              <div className="p-4 bg-slate-50 dark:bg-slate-950/40 border border-slate-100 dark:border-slate-900 rounded-xl">
                <p className="text-[10px] text-slate-400 font-bold uppercase">Career Readiness</p>
                <h3 className="text-xl font-bold text-slate-800 dark:text-slate-200">76% <span className="text-xs text-primary-500 font-normal">(Advanced)</span></h3>
                <div className="w-full bg-slate-200 dark:bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                  <div className="bg-secondary-500 h-full w-[76%]"></div>
                </div>
              </div>
              <div className="p-4 bg-slate-50 dark:bg-slate-950/40 border border-slate-100 dark:border-slate-900 rounded-xl">
                <p className="text-[10px] text-slate-400 font-bold uppercase">Missing Skills</p>
                <h3 className="text-xl font-bold text-red-500">5 Skills</h3>
                <div className="flex gap-1 mt-2">
                  <span className="bg-red-500/10 text-red-600 text-[8px] px-1.5 py-0.5 rounded font-bold">Docker</span>
                  <span className="bg-red-500/10 text-red-600 text-[8px] px-1.5 py-0.5 rounded font-bold">MLOps</span>
                </div>
              </div>
              <div className="p-4 bg-slate-50 dark:bg-slate-950/40 border border-slate-100 dark:border-slate-900 rounded-xl">
                <p className="text-[10px] text-slate-400 font-bold uppercase">Best Career Match</p>
                <h3 className="text-xl font-bold text-emerald-500">AI Engineer</h3>
                <p className="text-[10px] text-slate-400 mt-1">91% Match Index</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURE CARDS SECTION */}
      <section className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-t border-slate-100 dark:border-slate-900">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4">
            Platform Capabilities
          </h2>
          <p className="text-slate-500 dark:text-slate-400 max-w-xl mx-auto">
            Explore the five pillars of the AI Skill Accelerator designed to optimize your portfolio.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feat, idx) => (
            <div 
              key={idx}
              className="p-6 rounded-2xl border border-slate-200/50 dark:border-slate-800/40 bg-white/60 dark:bg-slate-900/30 backdrop-blur-md hover:-translate-y-1.5 hover:shadow-2xl hover:border-primary-500/25 transition-all duration-300 shadow-lg shadow-slate-100/10 dark:shadow-none hover:shadow-xl group animate-fade-in-up"
              style={{ animationDelay: `${idx * 100}ms` }}
            >
              <div className="p-3 bg-slate-50 dark:bg-slate-950 rounded-xl w-fit mb-4 border border-slate-100 dark:border-slate-900 group-hover:scale-110 group-hover:bg-primary-500/10 transition-all duration-300">
                {feat.icon}
              </div>
              <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2 group-hover:text-primary-500 transition-colors">{feat.title}</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{feat.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* HOW IT WORKS SECTION */}
      <section className="py-20 bg-slate-100/40 dark:bg-slate-900/10 border-t border-b border-slate-200/40 dark:border-slate-900 animate-fade-in-up">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4">
              How It Works
            </h2>
            <p className="text-slate-500 dark:text-slate-400 max-w-xl mx-auto">
              Follow these simple steps to accelerate your career readiness metrics.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {steps.map((st, idx) => (
              <div 
                key={idx} 
                className="relative flex flex-col items-start p-6 bg-white dark:bg-slate-900/40 border border-slate-200/40 dark:border-slate-800/40 rounded-2xl shadow-sm hover:shadow-md hover:border-secondary-500/20 transition-all duration-300 hover:-translate-y-1.5 animate-fade-in-up"
                style={{ animationDelay: `${idx * 100}ms` }}
              >
                <span className="absolute top-4 right-4 text-3xl font-extrabold text-slate-200 dark:text-slate-800 select-none">{st.num}</span>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2 mt-4">{st.title}</h3>
                <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{st.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* TESTIMONIALS SECTION */}
      <section className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4">
            Student Testimonials
          </h2>
          <p className="text-slate-500 dark:text-slate-400">
            Hear from students who transitioned from class assignments to corporate engineers.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200/40 dark:border-slate-800/40 rounded-2xl shadow-md hover:-translate-y-1.5 hover:shadow-xl hover:border-primary-500/20 transition-all duration-300 animate-fade-in-up delay-75">
            <div className="flex items-center space-x-3 mb-4">
              <div className="h-10 w-10 rounded-full bg-primary-100 dark:bg-primary-950 flex items-center justify-center text-primary-600 dark:text-primary-400 font-bold">SM</div>
              <div>
                <h4 className="text-sm font-bold text-slate-800 dark:text-slate-200">Sanjay Mohan</h4>
                <p className="text-[10px] text-slate-400">Now AI Engineer at TechCorp</p>
              </div>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed italic">
              "The Skill Gap analysis hit the nail on the head. I was missing MLOps and Docker from my resume. Following the roadmap got me hired in under 3 months."
            </p>
          </div>
          <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200/40 dark:border-slate-800/40 rounded-2xl shadow-md hover:-translate-y-1.5 hover:shadow-xl hover:border-primary-500/20 transition-all duration-300 animate-fade-in-up delay-150">
            <div className="flex items-center space-x-3 mb-4">
              <div className="h-10 w-10 rounded-full bg-secondary-100 dark:bg-secondary-950 flex items-center justify-center text-secondary-600 dark:text-secondary-400 font-bold">AK</div>
              <div>
                <h4 className="text-sm font-bold text-slate-800 dark:text-slate-200">Ananya Krish</h4>
                <p className="text-[10px] text-slate-400">Now Data Scientist at FinanceLab</p>
              </div>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed italic">
              "The Future Score Simulator is addicting. Checking off skills to see how my score increments motivated me to finish the courses. Highly recommended!"
            </p>
          </div>
          <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200/40 dark:border-slate-800/40 rounded-2xl shadow-md hover:-translate-y-1.5 hover:shadow-xl hover:border-primary-500/20 transition-all duration-300 animate-fade-in-up delay-200">
            <div className="flex items-center space-x-3 mb-4">
              <div className="h-10 w-10 rounded-full bg-emerald-100 dark:bg-emerald-950 flex items-center justify-center text-emerald-600 dark:text-emerald-400 font-bold">RM</div>
              <div>
                <h4 className="text-sm font-bold text-slate-800 dark:text-slate-200">Ragul Murugan</h4>
                <p className="text-[10px] text-slate-400">Full Stack Developer Intern</p>
              </div>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed italic">
              "The resume improver helped me rewrite my generic projects. It took my 'Worked on database' bullet and optimized it to a quantitative achievement statement!"
            </p>
          </div>
        </div>
      </section>

      {/* FAQ SECTION */}
      <section className="py-20 bg-slate-100/40 dark:bg-slate-900/10 border-t border-slate-200/40 dark:border-slate-900">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16 animate-fade-in-up">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-slate-500 dark:text-slate-400">
              Clear answers to your platform questions.
            </p>
          </div>

          <div className="space-y-4 animate-fade-in-up delay-100">
            {faqs.map((faq, idx) => (
              <div key={idx} className="border border-slate-200/60 dark:border-slate-800/60 rounded-xl overflow-hidden bg-white dark:bg-slate-900 hover:border-primary-500/15 transition-all">
                <button
                  onClick={() => setActiveFaq(activeFaq === idx ? null : idx)}
                  className="w-full flex items-center justify-between p-5 text-left font-semibold text-sm text-slate-800 dark:text-slate-200 hover:bg-slate-55 dark:hover:bg-slate-800/40 transition-colors"
                >
                  <span>{faq.q}</span>
                  <ChevronDown className={`h-4 w-4 text-slate-400 transition-transform duration-300 ${activeFaq === idx ? 'rotate-180' : ''}`} />
                </button>
                {activeFaq === idx && (
                  <div className="p-5 border-t border-slate-100 dark:border-slate-800/60 bg-slate-50/50 dark:bg-slate-950/20 text-xs text-slate-500 dark:text-slate-400 leading-relaxed animate-fade-in">
                    {faq.a}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CONTACT SECTION */}
      <section className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 animate-fade-in-up delay-150">
        <div className="bg-gradient-to-br from-primary-600 to-secondary-600 rounded-3xl p-8 md:p-12 text-white relative overflow-hidden shadow-2xl shadow-primary-500/20">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom_right,rgba(255,255,255,0.1),transparent_70%)] pointer-events-none"></div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center relative z-10">
            <div>
              <h2 className="text-3xl font-extrabold mb-4 leading-tight">Ready to Accelerate Your Career?</h2>
              <p className="text-primary-100 text-sm mb-8 max-w-md leading-relaxed">
                Join thousands of students optimizing their portfolios. Upload your resume and start learning what actually matters today.
              </p>
              <div className="flex items-center space-x-3 text-xs text-primary-200">
                <CheckCircle2 className="h-4 w-4 text-white" />
                <span>No Credit Card Required</span>
                <CheckCircle2 className="h-4 w-4 text-white" />
                <span>100% Free for College Students</span>
              </div>
            </div>
            
            {/* Simple Contact Form */}
            <form onSubmit={(e) => { e.preventDefault(); alert("Thanks for reaching out! We'll get back to you shortly."); }} className="bg-white dark:bg-slate-900 p-6 rounded-2xl text-slate-900 dark:text-slate-100 border border-white/10 shadow-xl space-y-4 hover:scale-[1.01] transition-all">
              <h3 className="font-bold text-base text-slate-800 dark:text-slate-200">Contact Us / Request Demo</h3>
              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Name</label>
                <input 
                  type="text" 
                  required
                  placeholder="Your Name" 
                  className="w-full text-xs p-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 focus:outline-none focus:border-primary-500" 
                />
              </div>
              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Email</label>
                <input 
                  type="email" 
                  required
                  placeholder="name@college.edu" 
                  className="w-full text-xs p-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 focus:outline-none focus:border-primary-500" 
                />
              </div>
              <button 
                type="submit" 
                className="w-full p-3 bg-primary-600 text-white rounded-lg font-semibold text-xs hover:bg-primary-700 transition-colors shadow-lg"
              >
                Send Message
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="py-8 border-t border-slate-200/50 dark:border-slate-900 bg-white dark:bg-slate-950 text-center text-xs text-slate-400 dark:text-slate-500">
        <p>&copy; {new Date().getFullYear()} AI Skill Accelerator. All rights reserved.</p>
        <p className="mt-1">Built with React, Flask, and SQLite.</p>
      </footer>
    </div>
  );
}

export default LandingPage;
