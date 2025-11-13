# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# import sqlite3
# import hashlib
# from datetime import datetime

# app = Flask(__name__)
# app.secret_key = 'change-this-secret-key-in-production-12345'

# # Database initialization
# def init_db():
#     conn = sqlite3.connect('training.db')
#     c = conn.cursor()
    
#     # Users table
#     c.execute('''CREATE TABLE IF NOT EXISTS users
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   username TEXT UNIQUE NOT NULL,
#                   password TEXT NOT NULL,
#                   email TEXT NOT NULL,
#                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
#     # Progress table
#     c.execute('''CREATE TABLE IF NOT EXISTS progress
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   user_id INTEGER,
#                   module_id INTEGER,
#                   completed BOOLEAN DEFAULT 0,
#                   completed_at TIMESTAMP,
#                   FOREIGN KEY (user_id) REFERENCES users(id))''')
    
#     # Video progress table
#     c.execute('''CREATE TABLE IF NOT EXISTS video_progress
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   user_id INTEGER,
#                   video_id INTEGER,
#                   watched BOOLEAN DEFAULT 0,
#                   FOREIGN KEY (user_id) REFERENCES users(id))''')
    
#     # Certificates table
#     c.execute('''CREATE TABLE IF NOT EXISTS certificates
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   user_id INTEGER,
#                   issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                   certificate_id TEXT UNIQUE,
#                   FOREIGN KEY (user_id) REFERENCES users(id))''')
    
#     conn.commit()
#     conn.close()

# # === Training modules data (with fixed YouTube embed URLs) ===
# MODULES = [
#     {
#         'id': 1,
#         'title': 'Introduction to AI',
#         'description': 'Fundamentals of Artificial Intelligence and Machine Learning',
#         'duration': '45 mins',
#         'icon': '',
#         'videos': [
#             {'id': 1, 'title': 'What is AI?', 'duration': '10:00', 'url': 'https://www.youtube.com/embed/rJ1Qao09CFI'},
#             {'id': 2, 'title': 'Machine Learning Basics', 'duration': '12:00', 'url': 'https://www.youtube.com/embed/ukzFI9rgwfU'},
#             {'id': 3, 'title': 'Neural Networks Explained', 'duration': '15:00', 'url': 'https://www.youtube.com/embed/jmmW0F0biz0'}
#         ]
#     },
#     {
#         'id': 2,
#         'title': 'AI in Insurance',
#         'description': 'Applications of AI in the Insurance Industry',
#         'duration': '50 mins',
#         'icon': '',
#         'videos': [
#             {'id': 4, 'title': 'AI for Risk Assessment', 'duration': '15:00', 'url': 'https://www.youtube.com/embed/ScMzIvxBSi4'},
#             {'id': 5, 'title': 'Claims Processing Automation', 'duration': '12:00', 'url': 'https://www.youtube.com/embed/JMUxmLyrhSk'},
#             {'id': 6, 'title': 'Fraud Detection with AI', 'duration': '18:00', 'url': 'https://www.youtube.com/embed/tgbNymZ7vqY'}
#         ]
#     },
#     {
#         'id': 3,
#         'title': 'AI in Compliance',
#         'description': 'Leveraging AI for Regulatory Compliance',
#         'duration': '40 mins',
#         'icon': '',
#         'videos': [
#             {'id': 7, 'title': 'AI-Powered Compliance Monitoring', 'duration': '12:00', 'url': 'https://www.youtube.com/embed/FZ4sG3yg1nY'},
#             {'id': 8, 'title': 'Regulatory Risk Management', 'duration': '15:00', 'url': 'https://www.youtube.com/embed/5qKCG8nbRzg'},
#             {'id': 9, 'title': 'Document Analysis & Review', 'duration': '13:00', 'url': 'https://www.youtube.com/embed/3Kq1MIfTWCE'}
#         ]
#     },
#     {
#         'id': 4,
#         'title': 'Ethics & Governance',
#         'description': 'Ethical AI Implementation and Governance',
#         'duration': '35 mins',
#         'icon': '',
#         'videos': [
#             {'id': 10, 'title': 'AI Ethics Principles', 'duration': '10:00', 'url': 'https://www.youtube.com/embed/xAoljeRJ3lU'},
#             {'id': 11, 'title': 'Bias & Fairness', 'duration': '12:00', 'url': 'https://www.youtube.com/embed/NJ0Hj3XwFJQ'},
#             {'id': 12, 'title': 'AI Governance Framework', 'duration': '13:00', 'url': 'https://www.youtube.com/embed/Y7X-8h1tW4o'}
#         ]
#     },
#     {
#         'id': 5,
#         'title': 'Future of AI',
#         'description': 'Emerging Trends and Future Applications',
#         'duration': '30 mins',
#         'icon': '',
#         'videos': [
#             {'id': 13, 'title': 'AI Trends 2025', 'duration': '10:00', 'url': 'https://www.youtube.com/embed/EwTZ2xpQwpA'},
#             {'id': 14, 'title': 'Generative AI Revolution', 'duration': '12:00', 'url': 'https://www.youtube.com/embed/ZK3O402wf1c'},
#             {'id': 15, 'title': 'AI Career Opportunities', 'duration': '8:00', 'url': 'https://www.youtube.com/embed/_n9ymIzhbV0'}
#         ]
#     }
# ]

# # === Top videos (unchanged) ===
# TOP_10_VIDEOS = [
#     {'id': 101, 'title': 'AI in 5 Minutes', 'duration': '5:00', 'thumbnail': ''},
#     {'id': 102, 'title': 'Machine Learning Explained', 'duration': '8:00', 'thumbnail': ''},
#     {'id': 103, 'title': 'Deep Learning Basics', 'duration': '10:00', 'thumbnail': ''},
#     {'id': 104, 'title': 'Natural Language Processing', 'duration': '7:00', 'thumbnail': ''},
#     {'id': 105, 'title': 'Computer Vision 101', 'duration': '9:00', 'thumbnail': ''},
#     {'id': 106, 'title': 'AI vs ML vs DL', 'duration': '6:00', 'thumbnail': ''},
#     {'id': 107, 'title': 'AI Applications Today', 'duration': '8:00', 'thumbnail': ''},
#     {'id': 108, 'title': 'AI Ethics & Privacy', 'duration': '7:00', 'thumbnail': ''},
#     {'id': 109, 'title': 'Chatbots & Virtual Assistants', 'duration': '6:00', 'thumbnail': ''},
#     {'id': 110, 'title': 'AI Career Guide', 'duration': '10:00', 'thumbnail': ''}
# ]


# @app.route('/module/<int:module_id>')
# def module(module_id):
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     module = next((m for m in MODULES if m['id'] == module_id), None)
#     if not module:
#         return redirect(url_for('dashboard'))
    
#     conn = sqlite3.connect('training.db')
#     c = conn.cursor()
    
#     # Get watched videos for this module
#     video_ids = [v['id'] for v in module['videos']]
#     watched_videos = []
#     if video_ids:
#         placeholders = ','.join('?' * len(video_ids))
#         c.execute(f'''
#             SELECT video_id FROM video_progress 
#             WHERE user_id=? AND video_id IN ({placeholders}) AND watched=1
#         ''', [session['user_id']] + video_ids)
#         watched_videos = [row[0] for row in c.fetchall()]
    
#     conn.close()
#     return render_template('module.html', module=module, watched_videos=watched_videos)

# @app.route('/')
# def index():
#     if 'user_id' in session:
#         return redirect(url_for('dashboard'))
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        
#         conn = sqlite3.connect('training.db')
#         c = conn.cursor()
#         c.execute('SELECT id, username FROM users WHERE username=? AND password=?', 
#                   (username, password))
#         user = c.fetchone()
#         conn.close()
        
#         if user:
#             session['user_id'] = user[0]
#             session['username'] = user[1]
#             return redirect(url_for('dashboard'))
#         else:
#             return render_template('login.html', error='Invalid credentials')
    
#     return render_template('login.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        
#         try:
#             conn = sqlite3.connect('training.db')
#             c = conn.cursor()
#             c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
#                       (username, password, email))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('login'))
#         except sqlite3.IntegrityError:
#             return render_template('login.html', error='Username already exists', register=True)
    
#     return render_template('login.html', register=True)

# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     conn = sqlite3.connect('training.db')
#     c = conn.cursor()
    
#     # Get user progress
#     progress = {}
#     for module in MODULES:
#         c.execute('SELECT completed FROM progress WHERE user_id=? AND module_id=?',
#                   (session['user_id'], module['id']))
#         result = c.fetchone()
#         progress[module['id']] = result[0] if result else 0
    
#     # Get video progress
#     c.execute('SELECT video_id FROM video_progress WHERE user_id=? AND watched=1',
#               (session['user_id'],))
#     watched_videos = [row[0] for row in c.fetchall()]
    
#     conn.close()
    
#     # Calculate overall progress
#     total_modules = len(MODULES)
#     completed_modules = sum(progress.values())
#     overall_progress = int((completed_modules / total_modules) * 100) if total_modules > 0 else 0
    
#     return render_template('dashboard.html', 
#                            modules=MODULES, 
#                            progress=progress,
#                            watched_videos=watched_videos,
#                            top_videos=TOP_10_VIDEOS,
#                            overall_progress=overall_progress,
#                            username=session['username'])

# @app.route('/module/<int:module_id>')
# def module(module_id):
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     module = next((m for m in MODULES if m['id'] == module_id), None)
#     if not module:
#         return redirect(url_for('dashboard'))
    
#     conn = sqlite3.connect('training.db')
#     c = conn.cursor()
    
#     # Get watched videos for this module
#     video_ids = [v['id'] for v in module['videos']]
#     if video_ids:
#         placeholders = ','.join('?' * len(video_ids))
#         c.execute(f'SELECT video_id FROM video_progress WHERE user_id=? AND video_id IN ({placeholders}) AND watched=1',
#                   [session['user_id']] + video_ids)
#         watched_videos = [row[0] for row in c.fetchall()]
#     else:
#         watched_videos = []
    
#     conn.close()
    
#     return render_template('module.html', module=module, watched_videos=watched_videos)

# @app.route('/complete_video', methods=['POST'])
# def complete_video():
#     if 'user_id' not in session:
#         return jsonify({'success': False, 'error': 'Not logged in'})
    
#     data = request.json
#     video_id = data.get('video_id')
    
#     conn = sqlite3.connect('training.db')
#     c = conn.cursor()
    
#     # Check if already exists
#     c.execute('SELECT id FROM video_progress WHERE user_id=? AND video_id=?',
#               (session['user_id'], video_id))
#     existing = c.fetchone()
    
#     if existing:
#         c.execute('UPDATE video_progress SET watched=1 WHERE user_id=? AND video_id=?',
#                   (session['user_id'], video_id))
#     else:
#         c.execute('INSERT INTO video_progress (user_id, video_id, watched) VALUES (?, ?, 1)',
#                   (session['user_id'], video_id))
    
#     conn.commit()
#     conn.close()
    
#     return jsonify({'success': True})

# @app.route('/complete_module', methods=['POST'])
# def complete_module():
#     if 'user_id' not in session:
#         return jsonify({'success': False, 'error': 'Not logged in'})
    
#     data = request.json
#     module_id = data.get('module_id')
    
#     conn = sqlite3.connect('training.db')
#     c = conn.cursor()
    
#     # Check if already exists
#     c.execute('SELECT id FROM progress WHERE user_id=? AND module_id=?',
#               (session['user_id'], module_id))
#     existing = c.fetchone()
    
#     if existing:
#         c.execute('UPDATE progress SET completed=1, completed_at=? WHERE user_id=? AND module_id=?',
#                   (datetime.now(), session['user_id'], module_id))
#     else:
#         c.execute('INSERT INTO progress (user_id, module_id, completed, completed_at) VALUES (?, ?, 1, ?)',
#                   (session['user_id'], module_id, datetime.now()))
    
#     conn.commit()
    
#     # Check if all modules completed
#     c.execute('SELECT COUNT(*) FROM progress WHERE user_id=? AND completed=1',
#               (session['user_id'],))
#     completed_count = c.fetchone()[0]
    
#     all_completed = completed_count >= len(MODULES)
    
#     conn.close()
    
#     return jsonify({'success': True, 'all_completed': all_completed})

# @app.route('/certificate')
# def certificate():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     conn = sqlite3.connect('training.db')
#     c = conn.cursor()
    
#     # Check if all modules completed
#     c.execute('SELECT COUNT(*) FROM progress WHERE user_id=? AND completed=1',
#               (session['user_id'],))
#     completed_count = c.fetchone()[0]
    
#     if completed_count < len(MODULES):
#         conn.close()
#         return redirect(url_for('dashboard'))
    
#     # Check if certificate already exists
#     c.execute('SELECT certificate_id, issued_at FROM certificates WHERE user_id=?',
#               (session['user_id'],))
#     cert = c.fetchone()
    
#     if not cert:
#         # Generate certificate
#         cert_id = f'AI-CERT-{session["user_id"]}-{datetime.now().strftime("%Y%m%d%H%M%S")}'
#         c.execute('INSERT INTO certificates (user_id, certificate_id) VALUES (?, ?)',
#                   (session['user_id'], cert_id))
#         conn.commit()
        
#         c.execute('SELECT certificate_id, issued_at FROM certificates WHERE user_id=?',
#                   (session['user_id'],))
#         cert = c.fetchone()
    
#     conn.close()
    
#     return render_template('certificate.html', 
#                            username=session['username'],
#                            certificate_id=cert[0],
#                            issued_date=cert[1])

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     init_db()
#     app.run(debug=True, host='0.0.0.0', port=5000)


from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'change-this-secret-key-in-production-12345'

# Database initialization
def init_db():
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  email TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Progress table
    c.execute('''CREATE TABLE IF NOT EXISTS progress
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  module_id INTEGER,
                  completed BOOLEAN DEFAULT 0,
                  completed_at TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    # Video progress table
    c.execute('''CREATE TABLE IF NOT EXISTS video_progress
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  video_id INTEGER,
                  watched BOOLEAN DEFAULT 0,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    # Certificates table
    c.execute('''CREATE TABLE IF NOT EXISTS certificates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  certificate_id TEXT UNIQUE,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

# === Training modules data ===
MODULES = [
    {
        'id': 1,
        'title': 'Introduction to AI',
        'description': 'Fundamentals of Artificial Intelligence and Machine Learning',
        'duration': '45 mins',
        'icon': '',
        'videos': [
            {'id': 1, 'title': 'What is AI?', 'duration': '10:00', 'url': 'https://www.youtube.com/embed/rJ1Qao09CFI'},
            {'id': 2, 'title': 'Machine Learning Basics', 'duration': '12:00', 'url': 'https://www.youtube.com/embed/ukzFI9rgwfU'},
            {'id': 3, 'title': 'Neural Networks Explained', 'duration': '15:00', 'url': 'https://www.youtube.com/embed/jmmW0F0biz0'}
        ]
    },
    {
        'id': 2,
        'title': 'AI in Insurance',
        'description': 'Applications of AI in the Insurance Industry',
        'duration': '50 mins',
        'icon': '',
        'videos': [
            {'id': 4, 'title': 'AI for Risk Assessment', 'duration': '15:00', 'url': 'https://www.youtube.com/embed/ScMzIvxBSi4'},
            {'id': 5, 'title': 'Claims Processing Automation', 'duration': '12:00', 'url': 'https://www.youtube.com/embed/JMUxmLyrhSk'},
            {'id': 6, 'title': 'Fraud Detection with AI', 'duration': '18:00', 'url': 'https://www.youtube.com/embed/tgbNymZ7vqY'}
        ]
    },
    {
        'id': 3,
        'title': 'AI in Compliance',
        'description': 'Leveraging AI for Regulatory Compliance',
        'duration': '40 mins',
        'icon': '',
        'videos': [
            {'id': 7, 'title': 'AI-Powered Compliance Monitoring', 'duration': '12:00', 'url': 'https://www.youtube.com/embed/FZ4sG3yg1nY'},
            {'id': 8, 'title': 'Regulatory Risk Management', 'duration': '15:00', 'url': 'https://www.youtube.com/embed/5qKCG8nbRzg'},
            {'id': 9, 'title': 'Document Analysis & Review', 'duration': '13:00', 'url': 'https://www.youtube.com/embed/3Kq1MIfTWCE'}
        ]
    },
    {
        'id': 4,
        'title': 'Ethics & Governance',
        'description': 'Ethical AI Implementation and Governance',
        'duration': '35 mins',
        'icon': '',
        'videos': [
            {'id': 10, 'title': 'AI Ethics Principles', 'duration': '10:00', 'url': 'https://www.youtube.com/embed/xAoljeRJ3lU'},
            {'id': 11, 'title': 'Bias & Fairness', 'duration': '12:00', 'url': 'https://www.youtube.com/embed/NJ0Hj3XwFJQ'},
            {'id': 12, 'title': 'AI Governance Framework', 'duration': '13:00', 'url': 'https://www.youtube.com/embed/Y7X-8h1tW4o'}
        ]
    },
    {
        'id': 5,
        'title': 'Future of AI',
        'description': 'Emerging Trends and Future Applications',
        'duration': '30 mins',
        'icon': '',
        'videos': [
            {'id': 13, 'title': 'AI Trends 2025', 'duration': '10:00', 'url': 'https://www.youtube.com/embed/EwTZ2xpQwpA'},
            {'id': 14, 'title': 'Generative AI Revolution', 'duration': '12:00', 'url': 'https://www.youtube.com/embed/ZK3O402wf1c'},
            {'id': 15, 'title': 'AI Career Opportunities', 'duration': '8:00', 'url': 'https://www.youtube.com/embed/_n9ymIzhbV0'}
        ]
    }
]

TOP_10_VIDEOS = [
    {'id': 101, 'title': 'AI in 5 Minutes', 'duration': '5:00', 'thumbnail': ''},
    {'id': 102, 'title': 'Machine Learning Explained', 'duration': '8:00', 'thumbnail': ''},
    {'id': 103, 'title': 'Deep Learning Basics', 'duration': '10:00', 'thumbnail': ''},
    {'id': 104, 'title': 'Natural Language Processing', 'duration': '7:00', 'thumbnail': ''},
    {'id': 105, 'title': 'Computer Vision 101', 'duration': '9:00', 'thumbnail': ''},
    {'id': 106, 'title': 'AI vs ML vs DL', 'duration': '6:00', 'thumbnail': ''},
    {'id': 107, 'title': 'AI Applications Today', 'duration': '8:00', 'thumbnail': ''},
    {'id': 108, 'title': 'AI Ethics & Privacy', 'duration': '7:00', 'thumbnail': ''},
    {'id': 109, 'title': 'Chatbots & Virtual Assistants', 'duration': '6:00', 'thumbnail': ''},
    {'id': 110, 'title': 'AI Career Guide', 'duration': '10:00', 'thumbnail': ''}
]

# ==== Routes 

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        
        conn = sqlite3.connect('training.db')
        c = conn.cursor()
        c.execute('SELECT id, username FROM users WHERE username=? AND password=?', 
                  (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        
        try:
            conn = sqlite3.connect('training.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                      (username, password, email))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('login.html', error='Username already exists', register=True)
    
    return render_template('login.html', register=True)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    progress = {}
    for module in MODULES:
        c.execute('SELECT completed FROM progress WHERE user_id=? AND module_id=?',
                  (session['user_id'], module['id']))
        result = c.fetchone()
        progress[module['id']] = result[0] if result else 0
    
    c.execute('SELECT video_id FROM video_progress WHERE user_id=? AND watched=1',
              (session['user_id'],))
    watched_videos = [row[0] for row in c.fetchall()]
    
    conn.close()
    
    total_modules = len(MODULES)
    completed_modules = sum(progress.values())
    overall_progress = int((completed_modules / total_modules) * 100) if total_modules > 0 else 0
    
    return render_template('dashboard.html', 
                           modules=MODULES, 
                           progress=progress,
                           watched_videos=watched_videos,
                           top_videos=TOP_10_VIDEOS,
                           overall_progress=overall_progress,
                           username=session['username'])

@app.route('/module/<int:module_id>')
def module(module_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    module = next((m for m in MODULES if m['id'] == module_id), None)
    if not module:
        return redirect(url_for('dashboard'))
    
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    video_ids = [v['id'] for v in module['videos']]
    if video_ids:
        placeholders = ','.join('?' * len(video_ids))
        c.execute(f'SELECT video_id FROM video_progress WHERE user_id=? AND video_id IN ({placeholders}) AND watched=1',
                  [session['user_id']] + video_ids)
        watched_videos = [row[0] for row in c.fetchall()]
    else:
        watched_videos = []
    
    conn.close()
    return render_template('module.html', module=module, watched_videos=watched_videos)

@app.route('/complete_video', methods=['POST'])
def complete_video():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    data = request.json
    video_id = data.get('video_id')
    
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    c.execute('SELECT id FROM video_progress WHERE user_id=? AND video_id=?',
              (session['user_id'], video_id))
    existing = c.fetchone()
    
    if existing:
        c.execute('UPDATE video_progress SET watched=1 WHERE user_id=? AND video_id=?',
                  (session['user_id'], video_id))
    else:
        c.execute('INSERT INTO video_progress (user_id, video_id, watched) VALUES (?, ?, 1)',
                  (session['user_id'], video_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/complete_module', methods=['POST'])
def complete_module():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    data = request.json
    module_id = data.get('module_id')
    
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    c.execute('SELECT id FROM progress WHERE user_id=? AND module_id=?',
              (session['user_id'], module_id))
    existing = c.fetchone()
    
    if existing:
        c.execute('UPDATE progress SET completed=1, completed_at=? WHERE user_id=? AND module_id=?',
                  (datetime.now(), session['user_id'], module_id))
    else:
        c.execute('INSERT INTO progress (user_id, module_id, completed, completed_at) VALUES (?, ?, 1, ?)',
                  (session['user_id'], module_id, datetime.now()))
    
    conn.commit()
    
    c.execute('SELECT COUNT(*) FROM progress WHERE user_id=? AND completed=1',
              (session['user_id'],))
    completed_count = c.fetchone()[0]
    
    all_completed = completed_count >= len(MODULES)
    
    conn.close()
    
    return jsonify({'success': True, 'all_completed': all_completed})

@app.route('/certificate')
def certificate():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('training.db')
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM progress WHERE user_id=? AND completed=1',
              (session['user_id'],))
    completed_count = c.fetchone()[0]
    
    if completed_count < len(MODULES):
        conn.close()
        return redirect(url_for('dashboard'))
    
    c.execute('SELECT certificate_id, issued_at FROM certificates WHERE user_id=?',
              (session['user_id'],))
    cert = c.fetchone()
    
    if not cert:
        cert_id = f'AI-CERT-{session["user_id"]}-{datetime.now().strftime("%Y%m%d%H%M%S")}'
        c.execute('INSERT INTO certificates (user_id, certificate_id) VALUES (?, ?)',
                  (session['user_id'], cert_id))
        conn.commit()
        
        c.execute('SELECT certificate_id, issued_at FROM certificates WHERE user_id=?',
                  (session['user_id'],))
        cert = c.fetchone()
    
    conn.close()
    
    return render_template('certificate.html', 
                           username=session['username'],
                           certificate_id=cert[0],
                           issued_date=cert[1])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ================= Main =================
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
