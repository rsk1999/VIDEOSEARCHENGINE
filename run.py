from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from datetime import timedelta
import os
import requests
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youtube_videos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize login_manager with the Flask app instance


@login_manager.user_loader
def load_user(user_id):
    # from user import User  # Adjust this import based on your project structure
    return User.query.get(int(user_id))

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

# Define routes and other functionalities

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Video(db.Model):
    __tablename__ = 'video'
    __table_args__ = {'extend_existing': True}  # Proper placement

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('videos', lazy=True))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            # If the user is not found, redirect them to the registration page
            flash('No account found with that username, please register.', 'info')
            return redirect(url_for('register'))

        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        
        else:
            # If the password does not match
            flash('Invalid login attempt.', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('search'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    
@app.route('/about')
def about():
    return render_template('about.html')
 
@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    videos = []
    keyword = "TRENDING"  # Default keyword if none provided
    if request.method == 'POST' and request.form.get('keyword'):
        keyword = request.form.get('keyword')

        # Search for videos
        video_api = "https://afyvb7t8u0.execute-api.us-east-1.amazonaws.com/prod/search_engine"
        video_data = {"query": keyword}
        video_response = requests.post(url=video_api, json=video_data)
        videos = json.loads(video_response.json()['body'])

    return render_template('search.html', videos=videos, keyword=keyword)


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    articles = []
    keyword = "expense management"  # Default keyword if none provided
    if request.method == 'POST' and request.form.get('keyword'):
        keyword = request.form.get('keyword')

        # Search for articles
        article_api = "https://newsapi.org/v2/everything"
        article_params = {
            'q': keyword,
            'language': 'en',
            'apiKey': "8f0325dacffe46a392f6aaebc202522c"  # Use your NewsAPI key
        }
        article_response = requests.get(article_api, params=article_params)
        articles = article_response.json().get('articles', [])

    return render_template('articles.html', articles=articles, keyword=keyword)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/save_videos', methods=['POST'])
@login_required
def save_videos():
    print("Form data:", request.form)
    selected_indices = request.form.getlist('video_ids[]')
    print("Selected video indices:", selected_indices)
    if not selected_indices:
        flash('No videos selected.', 'info')
        return redirect(url_for('search'))

    videos_saved = False
    for index in selected_indices:
        title = request.form.get(f'title_{index}')
        url = request.form.get(f'url_{index}')
        description = request.form.get(f'description_{index}')

        if title and url and description:
            if not Video.query.filter_by(url=url, user_id=current_user.id).first():
                video = Video(title=title, url=url, description=description, user_id=current_user.id)
                db.session.add(video)
                videos_saved = True

    if videos_saved:
        db.session.commit()
        flash('Videos saved successfully!', 'success')
    else:
        flash('No new videos added. They might already exist.', 'info')

    return redirect(url_for('search'))





@app.route('/delete_video/<int:video_id>', methods=['POST'])
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    flash('Video deleted successfully.', 'info')
    return redirect(url_for('saved_videos'))

@app.route('/saved_videos')
@login_required
def saved_videos():
    # Fetch videos saved by the current user
    videos = Video.query.filter_by(user_id=current_user.id).all()
    if not videos:
        flash('No saved videos to display.', 'info')
    return render_template('saved_videos.html', videos=videos)



@app.route('/handle_contact_form', methods=['POST'])
def handle_contact_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Logic to handle the message (e.g., save it to a database or send an email)
    flash('Thank you for your message, we will be in touch soon!', 'success')
    return redirect(url_for('contact'))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    try:
        if request.method == "GET":
            return render_template('forgot_password.html')
        elif request.method =="POST":
            email  = request.form['email']
            print("received post request")
    
            api = "https://9l5xftepoj.execute-api.us-east-1.amazonaws.com/OTP/otp_verification"
            data = {
                "path": "generate_otp",
                "userIdentifier": email
            }

            response = requests.post(url=api, json=data)
            data = response.json()
            print(data)

            return render_template('reset_password.html', email=email)
    except Exception as e:
        print(e)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    try:
        if request.method == "GET":
            return render_template('reset_password.html')
        else:
            email  = request.form['email']
            otp  = request.form['otp']
    
            api = "https://9l5xftepoj.execute-api.us-east-1.amazonaws.com/OTP/otp_verification"
    
            data = {
                "path": "verify_otp",
                "userIdentifier": email,
                "otp": otp,
            }
            response = requests.post(url=api, json=data)
            data = response.json()
            if data['verification']:
                pass
                new_password = request.form['new_password']
                user = User.query.filter_by(username=email).first()
                if user:
                    user.password = generate_password_hash(new_password)
                    db.session.commit()
                    print("password changed")
                    login_user(user)
                    return redirect(url_for('login'))

            return redirect(url_for('login'))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the tables
    app.run(debug=True)



