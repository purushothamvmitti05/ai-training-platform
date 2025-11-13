import sqlite3
from datetime import datetime
import hashlib

class Database:
    def __init__(self, db_name='training.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Create database connection"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Initialize all database tables"""
        conn = self.get_connection()
        c = conn.cursor()
        
        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Progress table
        c.execute('''CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            module_id INTEGER NOT NULL,
            completed BOOLEAN DEFAULT 0,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, module_id)
        )''')
        
        # Video progress table
        c.execute('''CREATE TABLE IF NOT EXISTS video_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            video_id INTEGER NOT NULL,
            watched BOOLEAN DEFAULT 0,
            watch_time INTEGER DEFAULT 0,
            watched_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, video_id)
        )''')
        
        # Certificates table
        c.execute('''CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            certificate_id TEXT UNIQUE NOT NULL,
            issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')
        
        # Quiz results table (bonus feature)
        c.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            module_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')
        
        conn.commit()
        conn.close()
        
        # Create demo user
        self.create_demo_user()
    
    def create_demo_user(self):
        """Create default demo user"""
        try:
            self.create_user('demo', 'demo123', 'demo@example.com', 'Demo User')
        except:
            pass  # User already exists
    
    # ========== USER OPERATIONS ==========
    
    def create_user(self, username, password, email, full_name=None):
        """Create a new user"""
        conn = self.get_connection()
        c = conn.cursor()
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            c.execute('''INSERT INTO users (username, password, email, full_name) 
                        VALUES (?, ?, ?, ?)''',
                     (username, hashed_password, email, full_name))
            conn.commit()
            user_id = c.lastrowid
            conn.close()
            return {'success': True, 'user_id': user_id}
        except sqlite3.IntegrityError:
            conn.close()
            return {'success': False, 'error': 'Username already exists'}
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        conn = self.get_connection()
        c = conn.cursor()
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        c.execute('''SELECT id, username, email, full_name FROM users 
                    WHERE username=? AND password=?''',
                 (username, hashed_password))
        user = c.fetchone()
        conn.close()
        
        if user:
            return {
                'success': True,
                'user': {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'full_name': user[3]
                }
            }
        return {'success': False, 'error': 'Invalid credentials'}
    
    def get_user_by_id(self, user_id):
        """Get user details by ID"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT id, username, email, full_name, created_at 
                    FROM users WHERE id=?''', (user_id,))
        user = c.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3],
                'created_at': user[4]
            }
        return None
    
    def get_all_users(self):
        """Get all users (admin function)"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT id, username, email, full_name, created_at 
                    FROM users ORDER BY created_at DESC''')
        users = c.fetchall()
        conn.close()
        
        return [{
            'id': u[0],
            'username': u[1],
            'email': u[2],
            'full_name': u[3],
            'created_at': u[4]
        } for u in users]
    
    # ========== MODULE PROGRESS OPERATIONS ==========
    
    def get_user_progress(self, user_id):
        """Get all module progress for a user"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT module_id, completed, completed_at 
                    FROM progress WHERE user_id=?''', (user_id,))
        progress = c.fetchall()
        conn.close()
        
        return {p[0]: {'completed': p[1], 'completed_at': p[2]} for p in progress}
    
    def mark_module_complete(self, user_id, module_id):
        """Mark a module as completed"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO progress (user_id, module_id, completed, completed_at) 
                        VALUES (?, ?, 1, ?)''',
                     (user_id, module_id, datetime.now()))
        except sqlite3.IntegrityError:
            c.execute('''UPDATE progress SET completed=1, completed_at=? 
                        WHERE user_id=? AND module_id=?''',
                     (datetime.now(), user_id, module_id))
        
        conn.commit()
        conn.close()
        return {'success': True}
    
    def is_module_completed(self, user_id, module_id):
        """Check if module is completed"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT completed FROM progress 
                    WHERE user_id=? AND module_id=?''', (user_id, module_id))
        result = c.fetchone()
        conn.close()
        
        return result[0] if result else False
    
    # ========== VIDEO PROGRESS OPERATIONS ==========
    
    def get_watched_videos(self, user_id):
        """Get all watched videos for a user"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT video_id, watch_time, watched_at 
                    FROM video_progress WHERE user_id=? AND watched=1''', (user_id,))
        videos = c.fetchall()
        conn.close()
        
        return [v[0] for v in videos]
    
    def mark_video_watched(self, user_id, video_id, watch_time=0):
        """Mark a video as watched"""
        conn = self.get_connection()
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO video_progress 
                        (user_id, video_id, watched, watch_time, watched_at) 
                        VALUES (?, ?, 1, ?, ?)''',
                     (user_id, video_id, watch_time, datetime.now()))
        except sqlite3.IntegrityError:
            c.execute('''UPDATE video_progress 
                        SET watched=1, watch_time=?, watched_at=? 
                        WHERE user_id=? AND video_id=?''',
                     (watch_time, datetime.now(), user_id, video_id))
        
        conn.commit()
        conn.close()
        return {'success': True}
    
    def is_video_watched(self, user_id, video_id):
        """Check if video is watched"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT watched FROM video_progress 
                    WHERE user_id=? AND video_id=?''', (user_id, video_id))
        result = c.fetchone()
        conn.close()
        
        return result[0] if result else False
    
    # ========== CERTIFICATE OPERATIONS ==========
    
    def get_certificate(self, user_id):
        """Get user's certificate"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT certificate_id, issued_at 
                    FROM certificates WHERE user_id=?''', (user_id,))
        cert = c.fetchone()
        conn.close()
        
        if cert:
            return {
                'certificate_id': cert[0],
                'issued_at': cert[1]
            }
        return None
    
    def issue_certificate(self, user_id):
        """Issue a certificate to user"""
        conn = self.get_connection()
        c = conn.cursor()
        
        # Check if certificate already exists
        c.execute('SELECT certificate_id FROM certificates WHERE user_id=?', (user_id,))
        existing = c.fetchone()
        
        if existing:
            conn.close()
            return {'success': True, 'certificate_id': existing[0]}
        
        # Generate certificate ID
        cert_id = f'AI-CERT-{user_id}-{datetime.now().strftime("%Y%m%d%H%M%S")}'
        
        c.execute('''INSERT INTO certificates (user_id, certificate_id) 
                    VALUES (?, ?)''', (user_id, cert_id))
        conn.commit()
        conn.close()
        
        return {'success': True, 'certificate_id': cert_id}
    
    def all_modules_completed(self, user_id, total_modules=5):
        """Check if all modules are completed"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''SELECT COUNT(*) FROM progress 
                    WHERE user_id=? AND completed=1''', (user_id,))
        count = c.fetchone()[0]
        conn.close()
        
        return count >= total_modules
    
    # ========== QUIZ OPERATIONS (BONUS) ==========
    
    def save_quiz_result(self, user_id, module_id, score, total_questions):
        """Save quiz result"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('''INSERT INTO quiz_results 
                    (user_id, module_id, score, total_questions) 
                    VALUES (?, ?, ?, ?)''',
                 (user_id, module_id, score, total_questions))
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def get_quiz_results(self, user_id, module_id=None):
        """Get quiz results for user"""
        conn = self.get_connection()
        c = conn.cursor()
        
        if module_id:
            c.execute('''SELECT score, total_questions, completed_at 
                        FROM quiz_results 
                        WHERE user_id=? AND module_id=? 
                        ORDER BY completed_at DESC''', (user_id, module_id))
        else:
            c.execute('''SELECT module_id, score, total_questions, completed_at 
                        FROM quiz_results 
                        WHERE user_id=? 
                        ORDER BY completed_at DESC''', (user_id,))
        
        results = c.fetchall()
        conn.close()
        
        return results
    
    # ========== STATISTICS ==========
    
    def get_user_statistics(self, user_id):
        """Get comprehensive user statistics"""
        conn = self.get_connection()
        c = conn.cursor()
        
        # Modules completed
        c.execute('''SELECT COUNT(*) FROM progress 
                    WHERE user_id=? AND completed=1''', (user_id,))
        modules_completed = c.fetchone()[0]
        
        # Videos watched
        c.execute('''SELECT COUNT(*) FROM video_progress 
                    WHERE user_id=? AND watched=1''', (user_id,))
        videos_watched = c.fetchone()[0]
        
        # Total watch time
        c.execute('''SELECT SUM(watch_time) FROM video_progress 
                    WHERE user_id=?''', (user_id,))
        total_watch_time = c.fetchone()[0] or 0
        
        # Certificate status
        c.execute('''SELECT certificate_id FROM certificates 
                    WHERE user_id=?''', (user_id,))
        has_certificate = c.fetchone() is not None
        
        conn.close()
        
        return {
            'modules_completed': modules_completed,
            'videos_watched': videos_watched,
            'total_watch_time': total_watch_time,
            'has_certificate': has_certificate
        }
    
    def get_platform_statistics(self):
        """Get overall platform statistics (admin)"""
        conn = self.get_connection()
        c = conn.cursor()
        
        # Total users
        c.execute('SELECT COUNT(*) FROM users')
        total_users = c.fetchone()[0]
        
        # Total certificates issued
        c.execute('SELECT COUNT(*) FROM certificates')
        total_certificates = c.fetchone()[0]
        
        # Total modules completed
        c.execute('SELECT COUNT(*) FROM progress WHERE completed=1')
        total_modules_completed = c.fetchone()[0]
        
        # Total videos watched
        c.execute('SELECT COUNT(*) FROM video_progress WHERE watched=1')
        total_videos_watched = c.fetchone()[0]
        
        conn.close()
        
        return {
            'total_users': total_users,
            'total_certificates': total_certificates,
            'total_modules_completed': total_modules_completed,
            'total_videos_watched': total_videos_watched
        }
    
    # ========== UTILITY FUNCTIONS ==========
    
    def reset_user_progress(self, user_id):
        """Reset all progress for a user"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('DELETE FROM progress WHERE user_id=?', (user_id,))
        c.execute('DELETE FROM video_progress WHERE user_id=?', (user_id,))
        c.execute('DELETE FROM quiz_results WHERE user_id=?', (user_id,))
        c.execute('DELETE FROM certificates WHERE user_id=?', (user_id,))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def delete_user(self, user_id):
        """Delete a user and all their data"""
        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute('DELETE FROM progress WHERE user_id=?', (user_id,))
        c.execute('DELETE FROM video_progress WHERE user_id=?', (user_id,))
        c.execute('DELETE FROM quiz_results WHERE user_id=?', (user_id,))
        c.execute('DELETE FROM certificates WHERE user_id=?', (user_id,))
        c.execute('DELETE FROM users WHERE id=?', (user_id,))
        
        conn.commit()
        conn.close()
        
        return {'success': True}


# Initialize database when module is imported
if __name__ == '__main__':
    db = Database()
    print("✅ Database initialized successfully!")
    print("✅ Demo user created: username='demo', password='demo123'")
    
    # Test database
    stats = db.get_platform_statistics()
    print(f"\n📊 Platform Statistics:")
    print(f"   Total Users: {stats['total_users']}")
    print(f"   Total Certificates: {stats['total_certificates']}")