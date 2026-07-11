import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        college TEXT,
        degree TEXT,
        graduation_year INTEGER,
        role TEXT DEFAULT 'user',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Profiles Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skills TEXT,
        interests TEXT,
        career_goal TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    # Resumes Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        extracted_text TEXT,
        uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    # ExtractedSkills Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS extracted_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_id INTEGER NOT NULL,
        skill_name TEXT NOT NULL,
        category TEXT,
        FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
    )
    ''')

    # JobRoles Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE NOT NULL,
        description TEXT,
        required_skills TEXT -- JSON List of skills
    )
    ''')

    # ATSReports Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ats_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resume_id INTEGER,
        job_role_id INTEGER,
        target_role_name TEXT,
        ats_score INTEGER,
        keyword_match INTEGER,
        skills_match INTEGER,
        projects_match INTEGER,
        experience_match INTEGER,
        formatting_score INTEGER,
        details TEXT, -- JSON structure of matches/mismatches
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    # CareerReadinessReports Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS career_readiness_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resume_id INTEGER,
        job_role_id INTEGER,
        target_role_name TEXT,
        readiness_score INTEGER,
        category TEXT, -- Beginner, Intermediate, Advanced, Industry Ready
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    # SkillGapReports Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skill_gap_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resume_id INTEGER,
        job_role_id INTEGER,
        target_role_name TEXT,
        matching_skills TEXT, -- JSON string list
        missing_skills TEXT, -- JSON string list
        strengths TEXT, -- JSON string list
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    # Roadmaps Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        job_role_id INTEGER,
        target_role_name TEXT,
        steps TEXT, -- JSON structure of milestones
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    # ProgressTracking Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        roadmap_id INTEGER NOT NULL,
        milestone_name TEXT NOT NULL,
        status TEXT DEFAULT 'pending', -- pending, completed
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE
    )
    ''')

    # ActivityLogs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        details TEXT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    # Seed Default Job Roles if empty
    cursor.execute("SELECT COUNT(*) FROM job_roles")
    if cursor.fetchone()[0] == 0:
        default_roles = [
            ("AI Engineer", "Design and deploy AI systems, Large Language Models (LLMs), RAG pipelines, and NLP solutions.", 
             ["Python", "PyTorch", "TensorFlow", "Transformers", "LLMs", "NLP", "OpenCV", "LangChain", "HuggingFace", "RAG", "Prompt Engineering", "Git", "Docker"]),
            ("Data Scientist", "Apply statistical analysis, predictive modeling, machine learning, and visualization techniques to extract insights.", 
             ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Statistics", "Machine Learning", "Data Visualization", "Tableau", "Matplotlib", "Seaborn", "Jupyter", "Git"]),
            ("Machine Learning Engineer", "Build, optimize, and scale production-ready machine learning models and end-to-end MLOps pipelines.", 
             ["Python", "TensorFlow", "Keras", "PyTorch", "MLOps", "Docker", "Kubernetes", "AWS", "MLflow", "Git", "FastAPI", "Linux"]),
            ("Data Analyst", "Cleanse, transform, and analyze datasets to create interactive reports, dashboards, and business insights.", 
             ["SQL", "Excel", "Python", "Pandas", "Tableau", "Power BI", "Statistics", "Data Cleaning", "Data Modeling", "Dashboarding", "Git"]),
            ("Full Stack Developer", "Develop frontend interfaces, backend APIs, manage state, and maintain persistent storage systems.", 
             ["JavaScript", "TypeScript", "React", "Node.js", "Express", "HTML", "CSS", "MongoDB", "PostgreSQL", "REST APIs", "Git", "Docker", "Next.js", "Tailwind CSS"]),
            ("DevOps Engineer", "Orchestrate CI/CD systems, configure cloud infrastructure, manage containerization, and supervise live infrastructure.", 
             ["Linux", "Bash", "Git", "Docker", "Kubernetes", "AWS", "Terraform", "Jenkins", "GitHub Actions", "CI/CD", "Nginx", "Prometheus"])
        ]
        for role, desc, skills in default_roles:
            cursor.execute(
                "INSERT INTO job_roles (title, description, required_skills) VALUES (?, ?, ?)",
                (role, desc, json.dumps(skills))
            )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
