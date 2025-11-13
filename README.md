# 🤖 AI Training Platform

A comprehensive web-based training platform for compliance professionals to learn about Artificial Intelligence.

#Features

-  **User Authentication** - Secure login and registration system
- **5 Comprehensive Modules** - Covering AI fundamentals to advanced applications
- **Top 10 AI Basics Videos** - Quick learning resources
- **Progress Tracking** - Visual dashboard showing completion status
-  **Certificate Generation** - Automatic certificate upon course completion
- **Responsive Design** - Works on desktop, tablet, and mobile
-  **Modern UI/UX** - Professional and intuitive interface

##  Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite
- **Deployment**: Render.com (recommended)

## Project Structure
```
ai-training-platform/
├── app.py                 # Main Flask application
├── database.py            # Database initialization
├── requirements.txt       # Python dependencies
├── training.db           # SQLite database (auto-generated)
├── static/
│   ├── css/
│   │   └── style.css     # All styling
│   └── js/
│       └── main.js       # Frontend JavaScript
├── templates/
│   ├── login.html        # Login/Register page
│   ├── dashboard.html    # Main dashboard
│   ├── module.html       # Module details page
│   └── certificate.html  # Certificate page
└── README.md             # This file
```

## Local Setup (Development)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
# Create project folder
mkdir ai-training-platform
cd ai-training-platform
```

### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

### Step 3: Initialize Database
```bash
# Run database setup
python database.py
```

This will create:
- `training.db` file
- 5 training modules with sample data
- Demo user account: `demo@test.com` / `demo123`

### Step 4: Run the Application
```bash
# Start Flask server
python app.py
```

The application will be available at: `http://localhost:5000`

### Step 5: Login
Use demo credentials:
- **Email**: demo@test.com
- **Password**: demo123

Or register a new account!

##  Deployment to Render.com (Free Hosting)

### Step 1: Prepare for Deployment

1. Create a `Procfile` in the root directory:
```
web: gunicorn app:app
```

2. Update `requirements.txt` to include:
```
Flask==3.0.0
Flask-Login==0.6.3
Werkzeug==3.0.1
gunicorn==21.2.0
```

3. Create `.gitignore` file:
```
__pycache__/
*.pyc
*.db
venv/
.env
```

### Step 2: Push to GitHub
```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AI Training Platform"

# Create new repository on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/ai-training-platform.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render.com

1. Go to [Render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ai-training-platform`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python database.py`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
5. Click "Create Web Service"

Wait 5-10 minutes for deployment to complete!

Your app will be live at: `https://ai-training-platform.onrender.com`

##  Alternative Deployment Options

### Option 1: PythonAnywhere (Free)

1. Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Upload your files via "Files" tab
3. Create a new web app (Flask)
4. Configure WSGI file to point to `app.py`
5. Reload the web app

### Option 2: Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Login and deploy
heroku login
heroku create ai-training-platform
git push heroku main
```

### Option 3: Railway.app

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway auto-detects Python and deploys

## 📝 Usage Guide

### For Students:

1. **Login/Register**
   - Use demo account or create new account
   - Email format validation included

2. **Dashboard**
   - View all 5 training modules
   - Track your progress (%)
   - Access Top 10 AI Basics videos

3. **Taking a Module**
   - Watch the training video
   - Review presentation materials
   - Read key takeaways
   - Click "Mark as Complete"

4. **Get Certificate**
   - Complete all 5 modules
   - Certificate button appears on dashboard
   - Print or download as PDF
   - Share on LinkedIn/Twitter

### For Administrators:

To add more modules, edit `database.py`:
```python
modules = [
    ('Module Title', 'Description', 'video_url', 'ppt_url', order, 'duration'),
    # Add more here
]
```

Then run: `python database.py`

##  Customization

### Change Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #2563eb;  /* Change this */
    --success-color: #10b981;  /* And this */
}
```

### Add More Modules
Edit the modules list in `database.py` and re-run initialization.

### Change Certificate Design
Edit `templates/certificate.html` and update styling in `style.css`.

## Security Notes

**IMPORTANT**: Before going to production:

1. Change the secret key in `app.py`:
```python
app.secret_key = 'GENERATE-A-SECURE-RANDOM-KEY-HERE'
```

Generate using:
```python
import secrets
print(secrets.token_hex(32))
```

2. Use password hashing (add to `app.py`):
```python
from werkzeug.security import generate_password_hash, check_password_hash

# When registering:
hashed_password = generate_password_hash(password)

# When logging in:
if check_password_hash(user['password'], password):
    # Login successful
```

3. Add HTTPS in production (Render.com does this automatically)

##  Troubleshooting

### Database errors
```bash
# Delete and recreate database
rm training.db
python database.py
```

### Module not found errors
```bash
# Ensure you're in the project directory
cd ai-training-platform
pip install -r requirements.txt
```

### Port already in use
```bash
# Run on different port
python app.py --port 5001
```

##  Database Schema

**Users Table**
- id (Primary Key)
- email (Unique)
- password
- name
- created_at

**Modules Table**
- id (Primary Key)
- title
- description
- video_url
- ppt_url
- order_number
- duration

**User Progress Table**
- id (Primary Key)
- user_id (Foreign Key)
- module_id (Foreign Key)
- completed (Boolean)
- completed_at (Timestamp)

**Certificates Table**
- id (Primary Key)
- user_id (Foreign Key)
- issued_at (Timestamp)
- certificate_number (Unique)

##  Demo Credentials

**Email**: demo@test.com  
**Password**: demo123

##  Support

For issues or questions:
1. Check this README
2. Review error messages in console
3. Check Flask logs: `python app.py` output

##  License

This project is created for educational purposes.

##  Future Enhancements

- [ ] Email notifications on certificate generation
- [ ] Quiz system for each module
- [ ] Admin panel for content management
- [ ] Discussion forums
- [ ] Mobile app version
- [ ] Multi-language support

---

**Made with  for Compliance Professionals**

Happy Learning! 
```

---

## Additional Setup Files

### File 11: `Procfile` (for deployment)
```
web: gunicorn app:app
```

### File 12: `.gitignore`
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.db
.DS_Store
.env
*.log
instance/
.pytest_cache/
.coverage
htmlcov/
