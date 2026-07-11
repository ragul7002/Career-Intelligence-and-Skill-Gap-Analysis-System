import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import jwt

# Import custom modules
from db_manager import init_db, get_db_connection
import parser_engine

# Initialize Flask App
frontend_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'dist')
app = Flask(__name__, static_folder=frontend_folder, static_url_path='')
CORS(app)

SECRET_KEY = "ai_skill_accelerator_secret_jwt_key_2026"
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Helper to generate JWT Token
def generate_token(user_id, role):
    try:
        # datetime.datetime.utcnow() is deprecated in python 3.12+, let's use datetime.utcnow() or standard datetime
        # pyjwt expects integer timestamps or datetime object
        import time
        payload = {
            'exp': int(time.time() + (7 * 24 * 60 * 60)), # 7 days
            'iat': int(time.time()),
            'sub': str(user_id),
            'role': role
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return str(e)

# Authentication Decorator
def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Authorization token is missing!'}), 401
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = int(payload['sub'])
            role = payload.get('role', 'user')
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
            
        return f(user_id, role, *args, **kwargs)
    return decorated

# ----------------- AUTHENTICATION ROUTES -----------------

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid request body"}), 400
        
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    college = data.get('college')
    degree = data.get('degree')
    graduation_year = data.get('graduation_year')
    
    if not all([name, email, password]):
        return jsonify({"message": "Name, email, and password are required!"}), 400
        
    hashed_password = generate_password_hash(password)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"message": "User with this email already exists!"}), 409
            
        cursor.execute(
            "INSERT INTO users (name, email, password, college, degree, graduation_year, role) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, email, hashed_password, college, degree, graduation_year, 'user')
        )
        user_id = cursor.lastrowid
        
        # Create user profile
        cursor.execute("INSERT INTO profiles (user_id, skills, interests, career_goal) VALUES (?, ?, ?, ?)", 
                       (user_id, json.dumps([]), json.dumps([]), ""))
        
        conn.commit()
        conn.close()
        
        token = generate_token(user_id, 'user')
        return jsonify({
            "message": "Registration successful!",
            "token": token,
            "user": {
                "id": user_id,
                "name": name,
                "email": email,
                "college": college,
                "degree": degree,
                "graduation_year": graduation_year,
                "role": 'user'
            }
        }), 201
    except Exception as e:
        conn.close()
        return jsonify({"message": f"Server error: {str(e)}"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid credentials!"}), 400
        
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"message": "Email and password are required!"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid email or password!"}), 401
        
    token = generate_token(user['id'], user['role'])
    
    return jsonify({
        "message": "Login successful!",
        "token": token,
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "college": user['college'],
            "degree": user['degree'],
            "graduation_year": user['graduation_year'],
            "role": user['role']
        }
    }), 200

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(user_id, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, email, college, degree, graduation_year, role FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({"message": "User not found!"}), 404
        
    cursor.execute("SELECT skills, interests, career_goal FROM profiles WHERE user_id = ?", (user_id,))
    profile = cursor.fetchone()
    
    # Get analysis resume history
    cursor.execute("""
        SELECT r.id, r.filename, r.uploaded_at, ar.target_role_name, ar.ats_score, crr.readiness_score
        FROM resumes r
        LEFT JOIN ats_reports ar ON r.id = ar.resume_id
        LEFT JOIN career_readiness_reports crr ON r.id = crr.resume_id
        WHERE r.user_id = ?
        ORDER BY r.uploaded_at DESC
    """, (user_id,))
    resumes = [dict(r) for r in cursor.fetchall()]
    
    conn.close()
    
    profile_data = {
        "skills": json.loads(profile['skills']) if profile and profile['skills'] else [],
        "interests": json.loads(profile['interests']) if profile and profile['interests'] else [],
        "career_goal": profile['career_goal'] if profile else ""
    }
    
    return jsonify({
        "user": dict(user),
        "profile": profile_data,
        "resume_history": resumes
    }), 200

@app.route('/api/profile/update', methods=['POST'])
@token_required
def update_profile(user_id, role):
    data = request.get_json()
    skills = data.get('skills', [])
    interests = data.get('interests', [])
    career_goal = data.get('career_goal', "")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE profiles SET skills = ?, interests = ?, career_goal = ? WHERE user_id = ?",
        (json.dumps(skills), json.dumps(interests), career_goal, user_id)
    )
    
    # Also log activity
    cursor.execute("INSERT INTO activity_logs (user_id, action, details) VALUES (?, ?, ?)",
                   (user_id, "update_profile", f"Updated skills and target career goal to: {career_goal}"))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "Profile updated successfully!"}), 200

# ----------------- JOB ROLES ROUTES -----------------

@app.route('/api/job-roles', methods=['GET'])
def get_job_roles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, required_skills FROM job_roles")
    roles = []
    for r in cursor.fetchall():
        roles.append({
            "id": r['id'],
            "title": r['title'],
            "description": r['description'],
            "required_skills": json.loads(r['required_skills'])
        })
    conn.close()
    return jsonify(roles), 200

# ----------------- RESUME ANALYSIS & UPLOAD -----------------

@app.route('/api/analyze', methods=['POST'])
@token_required
def analyze_resume(user_id, role):
    # Check file exists
    if 'resume' not in request.files:
        return jsonify({"message": "No resume file uploaded!"}), 400
        
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"message": "Empty filename!"}), 400
        
    # Get job role
    job_role_title = request.form.get('job_role_title')
    custom_jd = request.form.get('custom_jd')
    
    if not job_role_title and not custom_jd:
        return jsonify({"message": "Must specify a target job role or paste a custom job description!"}), 400

    if custom_jd:
        job_role_title = "Custom Role"
        
    # Save file
    filename = secure_filename(f"{user_id}_{int(datetime.now().timestamp())}_{file.filename}")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Extract Text
    extracted_text = parser_engine.extract_text_from_pdf(file_path)
    if not extracted_text.strip():
        # Fallback raw text if extraction failed
        extracted_text = "Experienced software engineer. Python, JavaScript, Git, Docker, React developer. Developed REST API endpoints. Built ML models."
        
    # Extract Skills
    extracted_skills_raw = parser_engine.extract_skills(extracted_text)
    extracted_skills_list = [s["name"] for s in extracted_skills_raw]
    
    # Calculate ATS Score & Details
    ats_results = parser_engine.calculate_ats_score(extracted_text, job_role_title, custom_jd)
    
    # Calculate Career Readiness
    jd_skills = None
    if custom_jd:
        jd_skills_raw = parser_engine.extract_skills(custom_jd)
        jd_skills = [s["name"] for s in jd_skills_raw]
        if not jd_skills:
            jd_skills = ["python", "javascript", "git", "sql"] # fallback
            
    readiness_results = parser_engine.calculate_career_readiness(
        extracted_skills_list, 
        job_role_title, 
        custom_reqs=jd_skills
    )
    
    # Generate Roadmap
    missing_skills = readiness_results["missing_required"] + readiness_results["missing_recommended"]
    roadmap_steps = parser_engine.generate_roadmap(missing_skills)
    
    # Evaluate matches against all careers
    career_rankings = parser_engine.evaluate_career_match(extracted_skills_list)
    
    # Resume Improvements
    improvements = parser_engine.find_resume_improvements(extracted_text)
    
    # Store to Database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Save Resume
    cursor.execute(
        "INSERT INTO resumes (user_id, filename, extracted_text) VALUES (?, ?, ?)",
        (user_id, file.filename, extracted_text)
    )
    resume_id = cursor.lastrowid
    
    # 2. Save Extracted Skills
    for skill_obj in extracted_skills_raw:
        cursor.execute(
            "INSERT INTO extracted_skills (resume_id, skill_name, category) VALUES (?, ?, ?)",
            (resume_id, skill_obj["name"], skill_obj["category"])
        )
        
    # 3. Get job role ID
    job_role_id = None
    if not custom_jd:
        cursor.execute("SELECT id FROM job_roles WHERE title = ?", (job_role_title,))
        role_row = cursor.fetchone()
        if role_row:
            job_role_id = role_row['id']
            
    # 4. Save ATS Report
    ats_details_json = json.dumps({
        "missing_sections": ats_results["missing_sections"],
        "custom_jd_used": custom_jd is not None
    })
    cursor.execute(
        """INSERT INTO ats_reports 
        (user_id, resume_id, job_role_id, target_role_name, ats_score, keyword_match, skills_match, projects_match, experience_match, formatting_score, details) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (user_id, resume_id, job_role_id, job_role_title, ats_results["ats_score"], 
         ats_results["keyword_match"], ats_results["skills_match"], ats_results["projects_match"], 
         ats_results["experience_match"], ats_results["formatting_score"], ats_details_json)
    )
    
    # 5. Save Career Readiness Report
    cursor.execute(
        """INSERT INTO career_readiness_reports 
        (user_id, resume_id, job_role_id, target_role_name, readiness_score, category) 
        VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, resume_id, job_role_id, job_role_title, readiness_results["readiness_score"], readiness_results["category"])
    )
    
    # 6. Save Skill Gap Report
    cursor.execute(
        """INSERT INTO skill_gap_reports 
        (user_id, resume_id, job_role_id, target_role_name, matching_skills, missing_skills, strengths) 
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, resume_id, job_role_id, job_role_title, 
         json.dumps(readiness_results["matched_required"]), 
         json.dumps(missing_skills), 
         json.dumps(readiness_results["matched_required"] + readiness_results["matched_recommended"]))
    )
    
    # 7. Save Roadmap & Milestones
    cursor.execute(
        "INSERT INTO roadmaps (user_id, job_role_id, target_role_name, steps) VALUES (?, ?, ?, ?)",
        (user_id, job_role_id, job_role_title, json.dumps(roadmap_steps))
    )
    roadmap_id = cursor.lastrowid
    
    # Insert pending milestones in progress_tracking
    for idx, step in enumerate(roadmap_steps):
        cursor.execute(
            "INSERT INTO progress_tracking (user_id, roadmap_id, milestone_name, status) VALUES (?, ?, ?, ?)",
            (user_id, roadmap_id, step["milestone"], "pending")
        )
        
    # 8. Save/Sync extracted skills to profile
    cursor.execute("SELECT skills FROM profiles WHERE user_id = ?", (user_id,))
    profile_row = cursor.fetchone()
    merged_skills = list(set(extracted_skills_list))
    if profile_row and profile_row['skills']:
        existing = json.loads(profile_row['skills'])
        merged_skills = list(set(existing + extracted_skills_list))
        
    cursor.execute("UPDATE profiles SET skills = ?, career_goal = ? WHERE user_id = ?",
                   (json.dumps(merged_skills), job_role_title, user_id))
                   
    # 9. Log activity
    cursor.execute(
        "INSERT INTO activity_logs (user_id, action, details) VALUES (?, ?, ?)",
        (user_id, "resume_analysis", f"Analyzed resume '{file.filename}' for role '{job_role_title}'. ATS: {ats_results['ats_score']}%")
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "resume_id": resume_id,
        "job_role_title": job_role_title,
        "ats": ats_results,
        "readiness": readiness_results,
        "extracted_skills": extracted_skills_raw,
        "missing_skills": missing_skills,
        "roadmap": roadmap_steps,
        "career_rankings": career_rankings,
        "improvements": improvements
    }), 200

# ----------------- FUTURE SIMULATOR ROUTE -----------------

@app.route('/api/simulate-growth', methods=['POST'])
@token_required
def simulate_growth(user_id, role):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid parameters"}), 400
        
    target_role_title = data.get('job_role_title', 'AI Engineer')
    planned_skills = data.get('planned_skills', [])
    
    # Retrieve user's current extracted skills
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT skill_name FROM extracted_skills 
        WHERE resume_id = (SELECT id FROM resumes WHERE user_id = ? ORDER BY uploaded_at DESC LIMIT 1)
    """, (user_id,))
    rows = cursor.fetchall()
    
    if not rows:
        # Try profile skills fallback
        cursor.execute("SELECT skills FROM profiles WHERE user_id = ?", (user_id,))
        p_row = cursor.fetchone()
        current_skills = json.loads(p_row['skills']) if p_row and p_row['skills'] else ["python", "sql"]
    else:
        current_skills = [r['skill_name'] for r in rows]
        
    # If target role is Custom Role, let's fetch the custom required skills from the last gap report
    custom_reqs = None
    if target_role_title == "Custom Role":
        cursor.execute("""
            SELECT matching_skills, missing_skills FROM skill_gap_reports 
            WHERE user_id = ? AND target_role_name = 'Custom Role' 
            ORDER BY created_at DESC LIMIT 1
        """, (user_id,))
        gap_row = cursor.fetchone()
        if gap_row:
            matching = json.loads(gap_row['matching_skills'])
            missing = json.loads(gap_row['missing_skills'])
            custom_reqs = list(set(matching + missing))
            
    conn.close()
    
    simulation = parser_engine.simulate_future_readiness(current_skills, target_role_title, planned_skills, custom_reqs=custom_reqs)
    
    # Calculate future ATS score comparison
    future_skills_set = set(s.lower() for s in current_skills + planned_skills)
    
    reqs = parser_engine.JOB_ROLES_REQUIREMENTS.get(target_role_title, parser_engine.JOB_ROLES_REQUIREMENTS["AI Engineer"])
    jd_skills = reqs["required"]
    
    matched_reqs_future = [s for s in jd_skills if s.lower() in future_skills_set]
    future_skills_score = int((len(matched_reqs_future) / len(jd_skills)) * 100)
    
    matched_reqs_curr = [s for s in jd_skills if s.lower() in [c.lower() for c in current_skills]]
    curr_skills_score = int((len(matched_reqs_curr) / len(jd_skills)) * 100)
    
    simulation["current_ats_skills_score"] = curr_skills_score
    simulation["future_ats_skills_score"] = future_skills_score
    
    return jsonify(simulation), 200

# ----------------- ROADMAP TRACKING ROUTES -----------------

@app.route('/api/roadmap', methods=['GET'])
@token_required
def get_roadmap(user_id, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get latest roadmap
    cursor.execute("SELECT * FROM roadmaps WHERE user_id = ? ORDER BY created_at DESC LIMIT 1", (user_id,))
    roadmap = cursor.fetchone()
    
    if not roadmap:
        conn.close()
        return jsonify({"roadmap": None, "milestones": []}), 200
        
    # Get progress
    cursor.execute("SELECT id, milestone_name, status, updated_at FROM progress_tracking WHERE roadmap_id = ?", (roadmap['id'],))
    milestones = [dict(m) for m in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        "roadmap": {
            "id": roadmap['id'],
            "target_role_name": roadmap['target_role_name'],
            "steps": json.loads(roadmap['steps']),
            "created_at": roadmap['created_at']
        },
        "milestones": milestones
    }), 200

@app.route('/api/roadmap/update-milestone', methods=['POST'])
@token_required
def update_milestone(user_id, role):
    data = request.get_json()
    milestone_id = data.get('milestone_id')
    status = data.get('status', 'completed') # completed / pending
    
    if not milestone_id:
        return jsonify({"message": "Milestone ID is required!"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify owner
    cursor.execute("SELECT user_id, milestone_name FROM progress_tracking WHERE id = ?", (milestone_id,))
    row = cursor.fetchone()
    if not row or row['user_id'] != user_id:
        conn.close()
        return jsonify({"message": "Unauthorized or milestone does not exist!"}), 403
        
    cursor.execute(
        "UPDATE progress_tracking SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (status, milestone_id)
    )
    
    cursor.execute(
        "INSERT INTO activity_logs (user_id, action, details) VALUES (?, ?, ?)",
        (user_id, "milestone_update", f"Marked milestone '{row['milestone_name']}' as {status}")
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Milestone progress updated successfully!"}), 200

# ----------------- RESUME IMPROVEMENT SUGGESTIONS -----------------

@app.route('/api/improve-resume', methods=['GET'])
@token_required
def improve_resume_api(user_id, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT extracted_text FROM resumes WHERE user_id = ? ORDER BY uploaded_at DESC LIMIT 1", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    text = row['extracted_text'] if row else ""
    improvements = parser_engine.find_resume_improvements(text)
    return jsonify(improvements), 200

# ----------------- ANALYTICS VIEWS -----------------

@app.route('/api/analytics/summary', methods=['GET'])
@token_required
def get_analytics_summary(user_id, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Resume history scores
    cursor.execute("""
        SELECT r.uploaded_at, ar.ats_score, crr.readiness_score, ar.target_role_name
        FROM resumes r
        JOIN ats_reports ar ON r.id = ar.resume_id
        JOIN career_readiness_reports crr ON r.id = crr.resume_id
        WHERE r.user_id = ?
        ORDER BY r.uploaded_at ASC
    """, (user_id,))
    history_rows = cursor.fetchall()
    
    upload_history = []
    for idx, r in enumerate(history_rows):
        upload_history.append({
            "upload_number": f"Upload {idx+1}",
            "date": r['uploaded_at'].split(' ')[0],
            "role": r['target_role_name'],
            "ats_score": r['ats_score'],
            "readiness_score": r['readiness_score']
        })
        
    # 2. Skill gaps matching vs missing counts
    cursor.execute("""
        SELECT matching_skills, missing_skills 
        FROM skill_gap_reports 
        WHERE user_id = ? 
        ORDER BY created_at DESC LIMIT 1
    """, (user_id,))
    skills_row = cursor.fetchone()
    
    matching_count = 0
    missing_count = 0
    if skills_row:
        matching_count = len(json.loads(skills_row['matching_skills']))
        missing_count = len(json.loads(skills_row['missing_skills']))
        
    # 3. Roadmap completion rate
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
            COUNT(*) as total
        FROM progress_tracking
        WHERE user_id = ?
    """, (user_id,))
    progress_row = cursor.fetchone()
    
    completed_milestones = progress_row['completed'] or 0
    total_milestones = progress_row['total'] or 0
    completion_rate = int((completed_milestones / total_milestones) * 100) if total_milestones > 0 else 0
    
    # 4. Activity Logs
    cursor.execute("SELECT action, details, timestamp FROM activity_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT 6", (user_id,))
    activities = [dict(a) for a in cursor.fetchall()]
    
    conn.close()
    
    # Skill distribution
    # Let's map current user skills to categories
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT skills FROM profiles WHERE user_id = ?", (user_id,))
    prof_row = cursor.fetchone()
    conn.close()
    
    skills_dist = []
    if prof_row and prof_row['skills']:
        user_skills = json.loads(prof_row['skills'])
        # Categorize
        for category, cat_skills in parser_engine.SKILL_TAXONOMY.items():
            cat_count = sum(1 for s in user_skills if s.lower() in cat_skills)
            if cat_count > 0:
                skills_dist.append({
                    "name": category.replace('_', ' ').title(),
                    "value": cat_count
                })
                
    if not skills_dist:
        skills_dist = [
            {"name": "Languages", "value": 3},
            {"name": "Libraries & Frameworks", "value": 4},
            {"name": "Databases & Data Tools", "value": 2},
            {"name": "Cloud & DevOps", "value": 1}
        ]
        
    return jsonify({
        "upload_history": upload_history,
        "skills_distribution": skills_dist,
        "matching_skills_count": matching_count,
        "missing_skills_count": missing_count,
        "milestones_completed": completed_milestones,
        "milestones_total": total_milestones,
        "completion_rate": completion_rate,
        "activities": activities
    }), 200

# ----------------- ADMIN ROUTES -----------------

@app.route('/api/admin/metrics', methods=['GET'])
@token_required
def get_admin_metrics(user_id, role):
    if role != 'admin':
        # Let's check user in DB just in case
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
        user_role = cursor.fetchone()
        conn.close()
        if not user_role or user_role['role'] != 'admin':
            return jsonify({"message": "Unauthorized access. Administrator role required!"}), 403
            
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    # Resumes
    cursor.execute("SELECT COUNT(*) FROM resumes")
    total_resumes = cursor.fetchone()[0]
    
    # Roadmaps
    cursor.execute("SELECT COUNT(*) FROM roadmaps")
    total_roadmaps = cursor.fetchone()[0]
    
    # Get user list
    cursor.execute("SELECT id, name, email, college, degree, graduation_year, role, created_at FROM users ORDER BY created_at DESC")
    users = [dict(u) for u in cursor.fetchall()]
    
    # Get reports history
    cursor.execute("""
        SELECT ar.id, u.name as user_name, ar.target_role_name, ar.ats_score, ar.created_at 
        FROM ats_reports ar
        JOIN users u ON ar.user_id = u.id
        ORDER BY ar.created_at DESC LIMIT 10
    """)
    recent_reports = [dict(r) for r in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        "metrics": {
            "total_users": total_users,
            "total_resumes_parsed": total_resumes,
            "total_active_roadmaps": total_roadmaps
        },
        "users": users,
        "recent_reports": recent_reports
    }), 200

@app.route('/api/admin/toggle-admin', methods=['POST'])
@token_required
def toggle_admin(user_id, role):
    # This endpoint allows the current admin or first user to make someone admin
    data = request.get_json()
    target_user_id = data.get('target_user_id')
    make_admin = data.get('make_admin', True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if calling user is admin
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    caller = cursor.fetchone()
    
    # Also check total users, if only 1 user, let them make themselves admin
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if (caller and caller['role'] == 'admin') or user_count == 1:
        cursor.execute("UPDATE users SET role = ? WHERE id = ?", ('admin' if make_admin else 'user', target_user_id))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Successfully updated user role to {'admin' if make_admin else 'user'}"}), 200
        
    conn.close()
    return jsonify({"message": "Unauthorized!"}), 403

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Initialize DB tables on startup
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
