# 📚 Setup Guide - Video Search Engine

This guide provides step-by-step instructions for setting up the Video Search Engine application on your local machine.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step-by-Step Setup](#step-by-step-setup)
3. [Configuration](#configuration)
4. [Database Initialization](#database-initialization)
5. [Running the Application](#running-the-application)
6. [Common Issues](#common-issues)

## Prerequisites

### Required Software
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **pip**: Comes bundled with Python 3.4+

### Verify Installation
```bash
# Check Python version
python --version
# or
python3 --version

# Check pip installation
pip --version

# Check Git installation
git --version
```

## Step-by-Step Setup

### 1. Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/rsk1999/VIDEOSEARCHENGINE.git

# Or using SSH
git clone git@github.com:rsk1999/VIDEOSEARCHENGINE.git

# Navigate to the project directory
cd VIDEOSEARCHENGINE
```

### 2. Create Virtual Environment

Creating a virtual environment isolates your project dependencies from system-wide packages.

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### 3. Install Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected packages:**
- Flask 3.0.3
- Flask-Login 0.6.3
- Flask-SQLAlchemy 3.1.1
- python-dotenv 1.0.0
- requests 2.31.0
- And other dependencies...

## Configuration

### 1. Create Environment Variable File

```bash
# Copy the example file
cp .env.example .env

# Or on Windows
copy .env.example .env
```

### 2. Edit Environment Variables

Open `.env` in your text editor and configure:

```env
# Generate a secure secret key
SECRET_KEY=your-secret-key-here

# Get your NewsAPI key from https://newsapi.org/
NEWS_API_KEY=your-newsapi-key

# Database configuration (default is fine for local development)
DATABASE_URI=sqlite:///youtube_videos.db
```

### 3. Generate a Secure SECRET_KEY

**Method 1 - Python:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Method 2 - Online Generator:**
Visit [randomkeygen.com](https://randomkeygen.com/) or similar

### 4. Obtain NewsAPI Key

1. Visit [newsapi.org](https://newsapi.org/)
2. Click "Get API Key"
3. Sign up for a free account
4. Copy your API key
5. Paste it in `.env` as `NEWS_API_KEY`

**Note:** The free tier allows 100 requests per day, which is sufficient for testing.

## Database Initialization

The database is automatically created when you first run the application.

```bash
# Run the application
python run.py
```

This will:
1. Create the `instance/` directory
2. Create `youtube_videos.db` SQLite database
3. Initialize the User and Video tables

**Manual Database Creation (if needed):**
```python
# Open Python shell
python

# In the Python shell:
from run import app, db
with app.app_context():
    db.create_all()
    print("Database created successfully!")
exit()
```

## Running the Application

### Development Mode

```bash
# Activate virtual environment first (if not already activated)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run the Flask application
python run.py
```

**Expected Output:**
```
 * Serving Flask app 'run'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

### Access the Application

Open your web browser and navigate to:
- **Local:** http://localhost:5000
- **Network:** http://127.0.0.1:5000

### Stop the Application

Press `Ctrl + C` in the terminal to stop the Flask server.

### Deactivate Virtual Environment

```bash
deactivate
```

## Common Issues

### Issue 1: Module Not Found Errors

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: Permission Denied (Windows)

**Error:**
```
venv\Scripts\activate : File cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Try activating again
venv\Scripts\activate
```

### Issue 3: Port Already in Use

**Error:**
```
Address already in use: Port 5000
```

**Solution:**
```bash
# Option 1: Kill the process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9

# Option 2: Use a different port
# Modify run.py, add at the end:
# app.run(debug=True, port=5001)
```

### Issue 4: Database Locked

**Error:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
```bash
# Close all connections to the database
# Delete the database file
rm instance/youtube_videos.db  # macOS/Linux
del instance\youtube_videos.db  # Windows

# Restart the application
python run.py
```

### Issue 5: Environment Variables Not Loading

**Error:**
```
KeyError: 'SECRET_KEY'
```

**Solution:**
```bash
# Verify .env file exists in project root
ls -la .env  # macOS/Linux
dir .env     # Windows

# Check .env file contains required variables
cat .env    # macOS/Linux
type .env   # Windows

# Ensure python-dotenv is installed
pip install python-dotenv
```

### Issue 6: API Request Failures

**Error:**
```
Failed to fetch videos/articles
```

**Solution:**
1. Check internet connection
2. Verify API keys in `.env` are correct
3. Test API key at [newsapi.org](https://newsapi.org/)
4. Check AWS endpoints are accessible
5. Verify you haven't exceeded API rate limits

## Next Steps

After successful setup:
1. ✅ Create a test user account
2. ✅ Search for videos
3. ✅ Save some favorites
4. ✅ Explore all features

For detailed feature usage, see the main [README.md](README.md).

## Getting Help

If you encounter issues not covered here:
1. Check the [main README](README.md) troubleshooting section
2. Review [API Documentation](API_DOCUMENTATION.md)
3. Open an issue on [GitHub](https://github.com/rsk1999/VIDEOSEARCHENGINE/issues)

---

Happy coding! 🚀
