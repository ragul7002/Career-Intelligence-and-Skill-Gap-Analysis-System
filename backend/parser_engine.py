import re
import json
import os
import math
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Fallbacks for PDF Parsing
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import pypdf
except ImportError:
    pypdf = None

# Comprehensive Skills Taxonomy
SKILL_TAXONOMY = {
    "languages": [
        "python", "javascript", "typescript", "c++", "c#", "java", "ruby", "php", 
        "rust", "go", "kotlin", "swift", "scala", "r", "sql", "html", "css", "bash", "shell"
    ],
    "libraries_frameworks": [
        "react", "node", "express", "flask", "django", "fastapi", "vue", "angular", 
        "next.js", "tailwind", "bootstrap", "pandas", "numpy", "scikit-learn", 
        "tensorflow", "pytorch", "keras", "transformers", "langchain", "huggingface", 
        "opencv", "nltk", "spacy", "matplotlib", "seaborn", "plotly", "jquery", "spring boot"
    ],
    "databases_data": [
        "postgresql", "mysql", "sqlite", "mongodb", "redis", "elasticsearch", 
        "cassandra", "dynamodb", "firebase", "mariadb", "oracle", "neo4j", 
        "tableau", "power bi", "looker", "excel", "hadoop", "spark", "hive", "kafka"
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible", 
        "jenkins", "github actions", "ci/cd", "git", "github", "gitlab", "bitbucket",
        "nginx", "apache", "prometheus", "grafana", "linux", "unix"
    ],
    "ai_ml_mlops": [
        "machine learning", "deep learning", "nlp", "natural language processing", 
        "computer vision", "mlops", "reinforcement learning", "prompt engineering", 
        "rag", "llm", "llms", "mlflow", "wandb", "neural networks"
    ]
}

# Flatten skills for general extraction
ALL_SKILLS = []
for category, skills in SKILL_TAXONOMY.items():
    ALL_SKILLS.extend(skills)

# Job Roles Default Config
JOB_ROLES_REQUIREMENTS = {
    "AI Engineer": {
        "required": ["python", "pytorch", "tensorflow", "transformers", "llms", "nlp", "langchain", "huggingface", "rag", "git", "docker"],
        "recommended": ["fastapi", "mlops", "prompt engineering", "gcp", "mongodb"],
        "description": "Develop LLM applications, retrieval-augmented generation pipelines, and cognitive search systems."
    },
    "Data Scientist": {
        "required": ["python", "sql", "pandas", "numpy", "scikit-learn", "statistics", "machine learning", "data visualization", "tableau", "git"],
        "recommended": ["r", "matplotlib", "seaborn", "spark", "jupyter"],
        "description": "Clean, model, and analyze large datasets to extract strategic insights and deploy predictive models."
    },
    "Machine Learning Engineer": {
        "required": ["python", "tensorflow", "pytorch", "mlops", "docker", "kubernetes", "aws", "git", "fastapi", "linux", "scikit-learn"],
        "recommended": ["c++", "mlflow", "wandb", "spark", "ci/cd"],
        "description": "Design, optimize, containerize, and scale machine learning models for production infrastructure."
    },
    "Data Analyst": {
        "required": ["sql", "excel", "python", "pandas", "tableau", "power bi", "statistics", "data cleaning", "dashboarding", "git"],
        "recommended": ["looker", "matplotlib", "seaborn", "mysql", "data modeling"],
        "description": "Transform messy data into clean databases, structured reporting pipelines, and interactive executive dashboards."
    },
    "Full Stack Developer": {
        "required": ["javascript", "typescript", "react", "node.js", "express", "html", "css", "mongodb", "postgresql", "git", "rest apis"],
        "recommended": ["next.js", "tailwind css", "docker", "next.js", "redis", "aws"],
        "description": "Develop full-stack web applications, stateful client designs, secure server endpoints, and relational databases."
    },
    "DevOps Engineer": {
        "required": ["linux", "bash", "git", "docker", "kubernetes", "aws", "terraform", "jenkins", "github actions", "ci/cd"],
        "recommended": ["nginx", "prometheus", "grafana", "ansible", "python", "azure"],
        "description": "Automate cloud deployment pipelines, orchestrate kubernetes containers, manage terraform IaC, and supervise server networks."
    }
}

# Skill learning times and milestone tasks for roadmap
SKILL_DETAILS = {
    "git": {"time": 1, "topics": ["VCS basics, staging, commits", "Branching, merging, conflict resolution", "Remote repositories, PR flows"]},
    "github": {"time": 1, "topics": ["GitHub profile setup", "Pull requests, issues, forks", "GitHub Pages deployment"]},
    "python": {"time": 3, "topics": ["Data types, structures (lists, dicts)", "Functions, OOP, error handling", "File operations, API requests"]},
    "sql": {"time": 2, "topics": ["SELECT queries, Joins, Grouping", "Subqueries, window functions", "DB schema design, indexing"]},
    "pandas": {"time": 2, "topics": ["DataFrames, series operations", "Data cleaning, filtering, aggregates", "Merging datasets, pivot tables"]},
    "numpy": {"time": 1, "topics": ["Vectorized arrays, indexing", "Mathematical functions", "Matrix operations"]},
    "scikit-learn": {"time": 3, "topics": ["Supervised learning (Regression, Classification)", "Model evaluation, train-test splits", "Feature scaling, hyperparameter tuning"]},
    "tensorflow": {"time": 4, "topics": ["Keras API, Sequential model", "Deep neural networks, activation functions", "Backpropagation, optimizers", "CNNs, RNNs"]},
    "pytorch": {"time": 4, "topics": ["Tensors, Autograd", "Custom model architectures", "Custom training loops", "DataLoader, transfer learning"]},
    "transformers": {"time": 3, "topics": ["Attention mechanisms", "Hugging Face Hub usage", "Fine-tuning models", "Pipeline API"]},
    "llms": {"time": 3, "topics": ["LLM API integrations", "Tokenization, context windows", "Quantization, model sizes"]},
    "nlp": {"time": 2, "topics": ["Tokenization, lemmatization", "TF-IDF, word embeddings", "Named Entity Recognition (NER)"]},
    "langchain": {"time": 2, "topics": ["Chains, Agents, Tools", "Memory management", "LCEL framework syntax"]},
    "huggingface": {"time": 2, "topics": ["HuggingFace spaces", "Pretrained models, tokenizers", "Model fine-tuning API"]},
    "rag": {"time": 3, "topics": ["Vector databases (ChromaDB, Pinecone)", "Document loading, text splitting", "Semantic search, generation validation"]},
    "docker": {"time": 2, "topics": ["Docker images, containers, commands", "Writing Dockerfiles", "Docker Compose multi-service setups"]},
    "kubernetes": {"time": 3, "topics": ["Pods, Deployments, Services", "ConfigMaps, Secrets", "Local setups (minikube, k3s)"]},
    "mlops": {"time": 3, "topics": ["Model registries, versioning", "MLflow tracking", "Deployment pipelines, model monitoring"]},
    "aws": {"time": 3, "topics": ["EC2 instances, S3 storage", "IAM permissions, security groups", "Lambda serverless, API Gateway"]},
    "gcp": {"time": 3, "topics": ["Google Compute Engine, GCS", "BigQuery analytics", "Vertex AI platforms"]},
    "terraform": {"time": 2, "topics": ["HCL syntax, providers", "Resources, variables, outputs", "State file management"]},
    "jenkins": {"time": 2, "topics": ["CI/CD pipelines, Jenkinsfile", "Build triggers, agents", "Plugin configurations"]},
    "github actions": {"time": 2, "topics": ["Workflow YAML syntax", "Secrets management", "Action marketplace integrations"]},
    "ci/cd": {"time": 2, "topics": ["Continuous integration principles", "Automated unit testing in pipe", "Deployment automation"]},
    "linux": {"time": 2, "topics": ["Command line navigation", "File permissions, ssh, scp", "Package management (apt, yum)"]},
    "fastapi": {"time": 2, "topics": ["Routing, Path parameters", "Pydantic request validation", "Async endpoints, CORS"]},
    "react": {"time": 3, "topics": ["Components, JSX, Props", "State management (useState, useEffect)", "Context API, Routing (React Router)"]},
    "node.js": {"time": 2, "topics": ["Event loop, NPM modules", "File system operations", "Express server setup"]},
    "express": {"time": 2, "topics": ["Middleware pipelines", "RESTful API route setup", "Error handling middlewares"]},
    "mongodb": {"time": 2, "topics": ["NoSQL document structures", "Mongoose schema modeling", "Aggregate query pipelines"]},
    "postgresql": {"time": 2, "topics": ["Relational schemas, foreign keys", "SQL optimizations", "Sequelize / Prisma ORM setup"]},
    "javascript": {"time": 2, "topics": ["ES6+ syntax (promises, async/await)", "DOM manipulations", "Fetch API / Axios requests"]},
    "typescript": {"time": 3, "topics": ["Types, interfaces, enums", "Strict typing, compiler configs", "React TypeScript integrations"]},
    "html": {"time": 1, "topics": ["Semantic tags structure", "Forms, SEO basic tags", "Accessibility standards"]},
    "css": {"time": 1, "topics": ["Box model, flexbox, grid", "Responsive media queries", "CSS variables, transitions"]},
    "tailwind css": {"time": 1, "topics": ["Utility class patterns", "Responsive styling prefixes", "Custom config properties"]}
}

# Resume Improvement suggestions map
RESUME_IMPROVEMENT_DATABASE = [
    {
        "pattern": r"(?i)(built|made|created)\s+(a\s+)?(ml|machine\s+learning|deep\s+learning)\s+model",
        "original": "Built ML model.",
        "improved": "Developed and optimized a supervised machine learning model (Random Forest), achieving 92% classification accuracy using Scikit-Learn and Python.",
        "reason": "Uses active verbs ('Developed', 'Optimized'), names specific algorithms/technologies, and specifies a quantitative result (92% accuracy)."
    },
    {
        "pattern": r"(?i)responsible\s+for\s+(the\s+)?(api|backend|endpoints)",
        "original": "Responsible for API backend.",
        "improved": "Designed, built, and deployed scalable RESTful API endpoints using Flask and PostgreSQL, reducing query latency by 35% through query indexing.",
        "reason": "Replaces passive duty statement ('Responsible for') with active execution verbs and measures operational improvement (35% latency reduction)."
    },
    {
        "pattern": r"(?i)helped\s+(with|in)\s+frontend",
        "original": "Helped with frontend UI.",
        "improved": "Spearheaded the design and integration of a responsive user interface using React.js and Tailwind CSS, increasing user session durations by 25%.",
        "reason": "Highlights leadership ('Spearheaded') and shows real product impact (25% user session duration increase)."
    },
    {
        "pattern": r"(?i)(did|worked\s+on)\s+database\s+stuff",
        "original": "Worked on database.",
        "improved": "Architected database schemas in MongoDB, writing custom aggregate pipelines that optimized data retrieval throughput by 40%.",
        "reason": "Replaces vague terms with professional terminology ('Architected', 'aggregate pipelines') and lists performance speedups."
    },
    {
        "pattern": r"(?i)(used|did|set\s+up)\s+docker\s+containers",
        "original": "Used docker containers.",
        "improved": "Orchestrated Docker containerization for 5 microservices, reducing deployment setup times by 50% using multi-stage builds and Docker Compose.",
        "reason": "Articulates exact technical complexity (5 microservices, multi-stage builds) and lists clear workflow acceleration metric."
    },
    {
        "pattern": r"(?i)wrote\s+python\s+scripts",
        "original": "Wrote python scripts.",
        "improved": "Automated ETL processing workflows in Python, cutting down manual reporting workloads by 12 hours weekly through pandas and cron job scripts.",
        "reason": "Highlights business utility (ETL automated, 12 hours saved) rather than just writing general code."
    }
]

def extract_text_from_pdf(file_path):
    """
    Extracts text from PDF files using pdfplumber with a pypdf fallback.
    """
    text = ""
    # Try pdfplumber
    if pdfplumber:
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
        except Exception as e:
            print(f"pdfplumber failed: {e}. Trying fallback.")
            
    # Try pypdf fallback
    if pypdf:
        try:
            with open(file_path, 'rb') as f:
                pdf = pypdf.PdfReader(f)
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
        except Exception as e:
            print(f"pypdf failed: {e}")
            
    # Standard text file read fallback (if someone uploaded a text file named as .pdf or similar)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Direct text read failed: {e}")
        
    return ""

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[\s+]+', ' ', text)
    return text

def extract_skills(text):
    """
    Extracts skills from text using regular expressions based on the taxonomy.
    Matches exact words to prevent partial matching (e.g., 'git' matching 'digital').
    """
    cleaned_text = clean_text(text)
    extracted = []
    
    # Skill matchers
    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            # Special regex escaping for skills like c++, next.js, scikit-learn, node.js
            escaped_skill = re.escape(skill)
            
            # Word boundary regex handling special chars
            if '+' in skill or '.' in skill or '-' in skill:
                # E.g. c++, next.js
                pattern = r'(?:^|[\s,;:\(\)\[\]])' + escaped_skill + r'(?:$|[\s,;:\(\)\[\]])'
            else:
                pattern = r'\b' + escaped_skill + r'\b'
                
            if re.search(pattern, cleaned_text):
                extracted.append({"name": skill, "category": category})
                
    return extracted

def calculate_ats_score(resume_text, job_role_title, custom_jd=None):
    """
    Calculates ATS score based on:
    - Keyword Match (20%)
    - Skills Match (30%)
    - Projects Match (20%)
    - Experience Match (20%)
    - Formatting Score (10%)
    """
    cleaned_resume = clean_text(resume_text)
    
    # Required skills setup
    if custom_jd:
        # Extract keywords using vectorizer comparing JD vs Resume
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf = vectorizer.fit_transform([cleaned_resume, clean_text(custom_jd)])
            cos_sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            keyword_score = int(cos_sim * 100)
        except Exception:
            keyword_score = 60
            
        # Try to extract skills from JD to evaluate Skill Match
        jd_skills_raw = extract_skills(custom_jd)
        jd_skills = [s["name"] for s in jd_skills_raw]
        
        if not jd_skills:
            jd_skills = ["python", "javascript", "git", "sql", "aws"] # Default fallback JD skills
    else:
        reqs = JOB_ROLES_REQUIREMENTS.get(job_role_title, JOB_ROLES_REQUIREMENTS["AI Engineer"])
        jd_skills = reqs["required"]
        
        # Simulating keyword match via standard required keywords
        matched_keywords_count = sum(1 for skill in jd_skills if re.search(r'\b' + re.escape(skill) + r'\b', cleaned_resume))
        keyword_score = int((matched_keywords_count / max(1, len(jd_skills))) * 100)
        # Cap range
        keyword_score = min(100, max(45, keyword_score + 15))

    # Skills Match
    extracted_skills_list = [s["name"].lower() for s in extract_skills(resume_text)]
    matched_skills = [skill for skill in jd_skills if skill.lower() in extracted_skills_list]
    skills_score = int((len(matched_skills) / max(1, len(jd_skills))) * 100)
    
    # Projects Match (Search for project sections, numbers, github profiles, deployment keywords)
    projects_score = 0
    project_keywords = ["project", "projects", "github", "git", "link", "deployed", "system", "built", "implemented"]
    project_hits = sum(1 for kw in project_keywords if kw in cleaned_resume)
    
    # Check if there is a 'projects' section heading
    has_project_section = 1 if re.search(r'\b(projects|personal projects|academic projects)\b', cleaned_resume) else 0
    projects_score = min(100, (project_hits * 8) + (has_project_section * 35))
    projects_score = max(35, projects_score) # Baseline if they have any text
    
    # Experience Match (Search for work experience, internships, job keywords, years)
    experience_score = 0
    exp_keywords = ["experience", "work", "intern", "internship", "job", "employment", "company", "position", "role"]
    exp_hits = sum(1 for kw in exp_keywords if kw in cleaned_resume)
    has_exp_section = 1 if re.search(r'\b(experience|work experience|professional experience|employment history)\b', cleaned_resume) else 0
    
    # Search for year patterns (e.g. "2022 - 2023", "1 year", "intern")
    years_matches = len(re.findall(r'\b(1|2|3|one|two|three)\s+year(s)?\s+experience\b', cleaned_resume))
    experience_score = min(100, (exp_hits * 10) + (has_exp_section * 25) + (years_matches * 15))
    experience_score = max(40, experience_score)
    
    # Formatting Score (Assess structure, sections, length)
    formatting_score = 100
    missing_sections = []
    for section in ["education", "skills", "projects", "experience"]:
        if not re.search(r'\b' + section + r'\b', cleaned_resume):
            formatting_score -= 15
            missing_sections.append(section)
            
    # Check length
    word_count = len(cleaned_resume.split())
    if word_count < 100:
        formatting_score -= 20
    elif word_count > 1000:
        formatting_score -= 10
        
    formatting_score = max(40, formatting_score)
    
    # Combined ATS Score
    total_ats = int(
        (keyword_score * 0.20) + 
        (skills_score * 0.30) + 
        (projects_score * 0.20) + 
        (experience_score * 0.20) + 
        (formatting_score * 0.10)
    )
    
    return {
        "ats_score": total_ats,
        "keyword_match": keyword_score,
        "skills_match": skills_score,
        "projects_match": projects_score,
        "experience_match": experience_score,
        "formatting_score": formatting_score,
        "missing_sections": missing_sections
    }

def calculate_career_readiness(extracted_skills, target_role_title, custom_reqs=None):
    """
    Calculates Career Readiness Score (0-100%) and returns category.
    Ready Categories:
    0-40: Beginner
    41-70: Intermediate
    71-90: Advanced
    91-100: Industry Ready
    """
    if custom_reqs:
        required_skills = custom_reqs
        recommended_skills = []
    else:
        reqs = JOB_ROLES_REQUIREMENTS.get(target_role_title, JOB_ROLES_REQUIREMENTS["AI Engineer"])
        required_skills = reqs["required"]
        recommended_skills = reqs["recommended"]
    
    skills_names = [s.lower() for s in extracted_skills]
    
    # Calculate core match (70% weight or 100% if custom)
    matched_reqs = [s for s in required_skills if s.lower() in skills_names]
    req_match_ratio = len(matched_reqs) / max(1, len(required_skills))
    
    # Calculate recommendation match
    if custom_reqs:
        matched_recs = []
        rec_match_ratio = 0
        missing_recs = []
        readiness_raw = req_match_ratio
    else:
        matched_recs = [s for s in recommended_skills if s.lower() in skills_names]
        rec_match_ratio = len(matched_recs) / max(1, len(recommended_skills))
        missing_recs = [s for s in recommended_skills if s.lower() not in skills_names]
        readiness_raw = (req_match_ratio * 0.75) + (rec_match_ratio * 0.25)
        
    readiness_score = int(readiness_raw * 100)
    
    # Set boundaries
    # Give base scores for standard resumes to simulate realistic score
    readiness_score = min(100, max(25, readiness_score))
    
    # Category allocation
    if readiness_score <= 40:
        category = "Beginner"
    elif readiness_score <= 70:
        category = "Intermediate"
    elif readiness_score <= 90:
        category = "Advanced"
    else:
        category = "Industry Ready"
        
    return {
        "readiness_score": readiness_score,
        "category": category,
        "matched_required": matched_reqs,
        "missing_required": [s for s in required_skills if s.lower() not in skills_names],
        "matched_recommended": matched_recs,
        "missing_recommended": missing_recs
    }

def simulate_future_readiness(extracted_skills, target_role_title, planned_skills, custom_reqs=None):
    """
    Simulates the Readiness and ATS improvements when user learns new skills.
    Returns:
    - Current Readiness, Future Readiness, Expected Growth
    - Current ATS, Future ATS
    - Estimated learning time in weeks
    """
    current_skills = [s.lower() for s in extracted_skills]
    future_skills = list(set(current_skills + [s.lower() for s in planned_skills]))
    
    # Current stats
    current_readiness = calculate_career_readiness(current_skills, target_role_title, custom_reqs)
    
    # Future stats
    future_readiness = calculate_career_readiness(future_skills, target_role_title, custom_reqs)
    
    # Estimated learning time calculation
    learning_time_weeks = 0
    for skill in planned_skills:
        skill_details = SKILL_DETAILS.get(skill.lower(), {"time": 2})
        learning_time_weeks += skill_details["time"]
        
    expected_growth = future_readiness["readiness_score"] - current_readiness["readiness_score"]
    
    # Generate Growth Projection Data (Graph representation)
    # We create weekly growth nodes
    growth_history = []
    weeks = max(1, learning_time_weeks)
    step_growth = expected_growth / weeks
    
    # Score progressions
    for i in range(weeks + 1):
        progress_readiness = min(100, current_readiness["readiness_score"] + int(step_growth * i))
        growth_history.append({
            "week": f"Week {i}",
            "readiness": progress_readiness
        })
        
    return {
        "current_readiness": current_readiness["readiness_score"],
        "future_readiness": future_readiness["readiness_score"],
        "current_category": current_readiness["category"],
        "future_category": future_readiness["category"],
        "expected_growth": expected_growth,
        "learning_time_weeks": learning_time_weeks,
        "growth_history": growth_history
    }

def generate_roadmap(missing_skills):
    """
    Generates a personalized month-by-month roadmap for missing skills.
    Each month contains milestone names, descriptions, checklist topics.
    """
    if not missing_skills:
        return []
        
    # Sort skills by learning sequence dependencies
    # E.g. git first, python next, libraries next, devops last
    def get_skill_order(skill_name):
        name = skill_name.lower()
        if name in ["git", "github"]:
            return 1
        elif name in ["python", "javascript", "sql"]:
            return 2
        elif name in ["pandas", "numpy", "html", "css"]:
            return 3
        elif name in ["react", "node.js", "express", "fastapi", "scikit-learn"]:
            return 4
        elif name in ["tensorflow", "pytorch", "transformers", "mongodb", "postgresql", "tailwind css"]:
            return 5
        elif name in ["docker", "llms", "nlp", "langchain", "huggingface", "rag"]:
            return 6
        else:
            return 7 # DevOps/Kubernetes/MLOps/Terraform/AWS
            
    sorted_missing = sorted(missing_skills, key=get_skill_order)
    
    roadmap_steps = []
    current_month = 1
    skills_in_month = []
    accumulated_weeks = 0
    
    for skill in sorted_missing:
        details = SKILL_DETAILS.get(skill.lower(), {"time": 2, "topics": [f"Introduction to {skill}", f"Intermediate concepts of {skill}", f"Practical project using {skill}"]})
        skills_in_month.append({
            "name": skill,
            "weeks": details["time"],
            "topics": details["topics"]
        })
        accumulated_weeks += details["time"]
        
        # When we hit ~4 weeks of work, we close the month
        if accumulated_weeks >= 4 or skill == sorted_missing[-1]:
            roadmap_steps.append({
                "month": f"Month {current_month}",
                "milestone": f"Master {' & '.join([s['name'] for s in skills_in_month])}",
                "skills": [s["name"] for s in skills_in_month],
                "weeks_total": accumulated_weeks,
                "tasks": [topic for s in skills_in_month for topic in s["topics"]],
                "project_prompt": f"Build a project integrating: {', '.join([s['name'] for s in skills_in_month])} to validate your learning."
            })
            current_month += 1
            skills_in_month = []
            accumulated_weeks = 0
            
    return roadmap_steps

def evaluate_career_match(extracted_skills_list):
    """
    Compares the user's resume against all standard job roles.
    Returns:
    - Ranked list of job matches with matching percentage
    - Why score is high, why score is low, missing skills
    """
    matches = []
    
    for title, config in JOB_ROLES_REQUIREMENTS.items():
        reqs = config["required"]
        matched_reqs = [r for r in reqs if r.lower() in [s.lower() for s in extracted_skills_list]]
        
        match_percentage = int((len(matched_reqs) / len(reqs)) * 100)
        # Cap reasonable ranges for display
        match_percentage = min(100, max(20, match_percentage))
        
        missing = [r for r in reqs if r.lower() not in [s.lower() for s in extracted_skills_list]]
        
        # High/low description generators
        if match_percentage >= 75:
            why_high = f"You possess critical required technologies like {', '.join(matched_reqs[:3])}."
            why_low = "Minor gaps exist in supplementary recommended toolsets."
        elif match_percentage >= 45:
            why_high = f"You have foundational skills like {', '.join(matched_reqs[:2]) if matched_reqs else 'programming fundamentals'}."
            why_low = f"You are missing key technologies: {', '.join(missing[:3])} which are heavily required."
        else:
            why_high = f"You have a baseline background in {matched_reqs[0] if matched_reqs else 'some IT domains'}."
            why_low = f"Major skill gaps detected. You must learn core concepts: {', '.join(missing[:4])}."
            
        matches.append({
            "role": title,
            "match_percent": match_percentage,
            "why_high": why_high,
            "why_low": why_low,
            "missing_skills": missing
        })
        
    # Sort matches descending
    return sorted(matches, key=lambda x: x["match_percent"], reverse=True)

def find_resume_improvements(resume_text):
    """
    Evaluates resume text for passive sentences and matches them to active suggestions.
    """
    improvements = []
    
    # Split text into lines/bullet points
    lines = [line.strip() for line in resume_text.split('\n') if len(line.strip()) > 10]
    
    for line in lines:
        for item in RESUME_IMPROVEMENT_DATABASE:
            if re.search(item["pattern"], line):
                # Avoid duplicates
                if not any(imp["original"] == line for imp in improvements):
                    improvements.append({
                        "original": line,
                        "improved": item["improved"],
                        "reason": item["reason"]
                    })
                    break
                    
    # If no improvements are triggered, provide default standard templates
    if not improvements:
        improvements = [
            {
                "original": "Built ML model.",
                "improved": "Developed and optimized a supervised machine learning model (Random Forest), achieving 92% classification accuracy using Scikit-Learn and Python.",
                "reason": "Uses active verbs ('Developed', 'Optimized'), names specific algorithms/technologies, and specifies a quantitative result (92% accuracy)."
            },
            {
                "original": "Responsible for API backend.",
                "improved": "Designed, built, and deployed scalable RESTful API endpoints using Flask and PostgreSQL, reducing query latency by 35% through query indexing.",
                "reason": "Replaces passive duty statement ('Responsible for') with active execution verbs and measures operational improvement (35% latency reduction)."
            },
            {
                "original": "Worked on database.",
                "improved": "Architected database schemas in MongoDB, writing custom aggregate pipelines that optimized data retrieval throughput by 40%.",
                "reason": "Replaces vague terms with professional terminology ('Architected', 'aggregate pipelines') and lists performance speedups."
            }
        ]
        
    return improvements[:4] # Return at most 4 suggestions

if __name__ == '__main__':
    # Dry run test
    test_text = "Experienced Developer with Python, Git, SQL, Docker, and React. Built ML model. Responsible for API backend."
    skills = extract_skills(test_text)
    print("Skills extracted:", [s["name"] for s in skills])
    
    ats = calculate_ats_score(test_text, "AI Engineer")
    print("ATS Score:", ats)
    
    readiness = calculate_career_readiness([s["name"] for s in skills], "AI Engineer")
    print("Career Readiness:", readiness)
    
    matches = evaluate_career_match([s["name"] for s in skills])
    print("Top match:", matches[0])
    
    improvements = find_resume_improvements(test_text)
    print("Improvements found:", len(improvements))
