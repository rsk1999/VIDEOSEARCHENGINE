from flask import Flask, request, jsonify, render_template
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()  # This will load the environment variables from the .env file


# Create a Flask application
app = Flask(__name__)

# Use an environment variable for the API key to keep it secure
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
print("Using API Key:", YOUTUBE_API_KEY)
def youtube_search(query, max_results=50):
    """Search YouTube videos by query using the YouTube Data API."""
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
     
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        type="video"
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId']
        print(search_result)
        video_title = search_result['snippet']['title']
        video_description = search_result['snippet']['description']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({'title': video_title, 'url': video_url, 'description': video_description})

    return videos


@app.route('/api/search', methods=['GET'])
def search_videos():
    keyword = request.args.get('keyword')
    print(f"Received keyword: {keyword}")  # Simple debug statement to check input
    if not keyword:
        return jsonify({'error': 'Missing keyword parameter'}), 400

    videos = youtube_search(keyword)
    return jsonify(videos)

@app.route('/')
def index():
    return render_template('index.html')




# @app.route('/api/search', methods=['GET'])
# def search_videos():
#     """API endpoint to search videos based on the 'keyword' query parameter."""
#     keyword = request.args.get('keyword')
#     if not keyword:
#         return jsonify({'error': 'Missing keyword parameter'}), 400

#     videos = youtube_search(keyword)
#     return jsonify(videos)

if __name__ == '__main__':
    app.run(debug=True)
    
    
