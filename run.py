from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# from googleapiclient.discovery import build
import os
import requests
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youtube_videos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text, nullable=True)

# YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
# YOUTUBE_API_SERVICE_NAME = "youtube"
# YOUTUBE_API_VERSION = "v3"

# def youtube_search(query, max_results=10):
#     youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
#     search_response = youtube.search().list(
#         q=query,
#         part="id,snippet",
#         maxResults=max_results,
#         type="video"
#     ).execute()

#     videos = []
#     for search_result in search_response.get('items', []):
#         video_id = search_result['id']['videoId']
#         video_title = search_result['snippet']['title']
#         video_url = f"https://www.youtube.com/watch?v={video_id}"
#         videos.append({'title': video_title, 'url': video_url, 'description': search_result['snippet']['description']})
#     return videos


@app.route('/', methods=['GET', 'POST'])
def index():
    videos = []
    articles = []
    keyword = "expense management"  # Default keyword if none provided
    if request.method == 'POST' and request.form.get('keyword'):
        keyword = request.form.get('keyword')

        # Search for videos
        video_api = "https://afyvb7t8u0.execute-api.us-east-1.amazonaws.com/prod/search_engine"
        video_data = {"query": keyword}
        video_response = requests.post(url=video_api, json=video_data)
        videos = json.loads(video_response.json()['body'])

        # Search for articles
        article_api = "https://newsapi.org/v2/everything"
        article_params = {
            'q': keyword,
            'language': 'en',
            'apiKey': "8f0325dacffe46a392f6aaebc202522c"  # Use your NewsAPI key
        }
        article_response = requests.get(article_api, params=article_params)
        articles = article_response.json().get('articles', [])

    return render_template('index.html', videos=videos, articles=articles, keyword=keyword)


@app.route('/save', methods=['POST'])
def save_video():
    video_ids = request.form.getlist('video_ids')
    if video_ids:
        for video_id in video_ids:
            title = request.form[f'title_{video_id}']
            url = request.form[f'url_{video_id}']
            description = request.form[f'description_{video_id}']
            if not Video.query.filter_by(url=url).first():  # Avoid duplicates
                video = Video(title=title, url=url, description=description)
                db.session.add(video)
                db.session.commit()
                flash('Video saved successfully!', 'success')
            else:
                flash('Video already saved.', 'info')
    return redirect(url_for('index'))

@app.route('/saved_videos')
def saved_videos():
    videos = Video.query.all()
    return render_template('saved_videos.html', videos=videos)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the tables
    app.run(debug=True)

