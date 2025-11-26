# 🎥 Video Search Engine (VIDVAULT)

A Flask-based web application that allows users to search for YouTube videos and news articles, save their favorites, and manage their content in one centralized platform.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🔐 **User Authentication**: Secure registration and login system with Flask-Login
- 🔍 **Video Search**: Search YouTube videos using AWS-backed API
- 📰 **Article Search**: Search news articles via NewsAPI integration
- 💾 **Save Favorites**: Save and manage your favorite videos
- 🔑 **Password Recovery**: OTP-based password reset functionality
- 📱 **Responsive Design**: Bootstrap 5 responsive UI with modern styling
- 🎨 **Smooth Animations**: Enhanced UX with Animate.css

## 🚀 Technologies Used

### Backend
- **Flask 3.0.3** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-Login** - User session management
- **SQLite** - Lightweight database
- **Python-dotenv** - Environment variable management

### Frontend
- **Bootstrap 5** - Responsive UI framework
- **Font Awesome** - Icon library
- **Animate.css** - CSS animations
- **Poppins Font** - Google Fonts typography

### External APIs
- **AWS API Gateway** - Video search endpoint
- **AWS Lambda** - OTP verification service
- **NewsAPI** - Article search service

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/rsk1999/VIDEOSEARCHENGINE.git
cd VIDEOSEARCHENGINE
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root by copying the example:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
SECRET_KEY=your-secret-key-here-generate-a-random-one
NEWS_API_KEY=your-newsapi-key-from-newsapi.org
DATABASE_URI=sqlite:///youtube_videos.db
```

**Getting API Keys:**
- **NewsAPI Key**: Sign up at [newsapi.org](https://newsapi.org/) for a free API key
- **SECRET_KEY**: Generate a random string (e.g., using `python -c "import secrets; print(secrets.token_hex(32))"`)

### 5. Initialize Database & Run
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
VIDEOSEARCHENGINE/
├── run.py                  # Main Flask application
├── wsgi.py                 # WSGI entry point for deployment
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.example           # Example environment file
├── .gitignore             # Git ignore rules
├── Procfile               # Deployment configuration
├── instance/              # Database storage
│   └── youtube_videos.db  # SQLite database
├── static/                # Static assets
│   ├── css/
│   │   └── styles.css     # Custom styles
│   ├── js/
│   │   └── scripts.js     # Custom JavaScript
│   └── img/
│       └── logo.png       # Application logo
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── home.html          # Homepage
    ├── search.html        # Video search
    ├── articles.html      # Article search
    ├── saved_videos.html  # User's saved videos
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── forgot_password.html
    ├── reset_password.html
    ├── about.html         # About page
    └── contact.html       # Contact page
```

## 🎮 Usage

### 1. Create an Account
- Navigate to the registration page
- Enter a username and password
- You'll be automatically logged in

### 2. Search for Videos
- Go to the search page
- Enter keywords (e.g., "Python tutorials")
- Browse results with embedded YouTube players
- Select videos to save to your favorites

### 3. Search for Articles
- Visit the Articles page
- Enter topics you're interested in
- Read the latest news articles

### 4. Manage Saved Videos
- Access your saved videos from the navigation menu
- View all your favorite content in one place
- Delete videos you no longer need

### 5. Password Reset
- Click "Forgot Password" on the login page
- Enter your email to receive an OTP
- Verify OTP and set a new password

## 🔒 Security Features

- ✅ Passwords hashed with Werkzeug security
- ✅ Session management with 5-minute timeout
- ✅ Environment variables for sensitive data
- ✅ CSRF protection via Flask
- ✅ SQL injection protection via SQLAlchemy ORM

## 🐛 Troubleshooting

### Application won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.8+)
- Verify `.env` file exists and contains required variables

### Database errors
- Delete the database file: `rm instance/youtube_videos.db`
- Restart the application to recreate tables

### API errors
- Verify NewsAPI key is valid in `.env`
- Check internet connection for external API calls
- Ensure AWS endpoints are accessible

### Video thumbnails not loading
- Check YouTube embed URLs are properly formatted
- Verify videos are still publicly available

## 📝 API Endpoints

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed endpoint documentation.

### Quick Reference
- `/` - Homepage
- `/login` - User login
- `/register` - User registration
- `/search` - Video search
- `/articles` - Article search
- `/saved_videos` - User's saved videos
- `/logout` - User logout

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**rsk1999**
- GitHub: [@rsk1999](https://github.com/rsk1999)

## 🙏 Acknowledgments

- Bootstrap for the UI components
- Font Awesome for icons
- NewsAPI for article data
- Flask community for excellent documentation

## 📧 Support

For support, email your-email@example.com or open an issue in the GitHub repository.

---

Made with ❤️ by rsk1999
