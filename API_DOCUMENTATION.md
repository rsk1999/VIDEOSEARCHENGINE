# 📖 API Documentation - Video Search Engine

Complete documentation for all API endpoints, request/response formats, and usage examples.

## Table of Contents
- [Authentication Endpoints](#authentication-endpoints)
- [Video Management](#video-management)
- [Article Search](#article-search)
- [Static Pages](#static-pages)
- [Request/Response Examples](#requestresponse-examples)

## Base URL

```
http://localhost:5000
```

## Authentication Endpoints

### Register New User

Create a new user account.

**Endpoint:** `POST /register`

**Request Type:** Form Data

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| username | string | Yes | Unique username (email format recommended) |
| password | string | Yes | User password (will be hashed) |

**Response:**
- **Success:** Redirect to `/search` (user logged in)
- **Error:** Redirect to `/register` with flash message

**Example Form:**
```html
<form method="POST" action="/register">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <button type="submit">Register</button>
</form>
```

**Error Cases:**
- Username already exists: Flash message "Username already exists!"

---

### User Login

Authenticate an existing user.

**Endpoint:** `POST /login`

**Request Type:** Form Data

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| username | string | Yes | Registered username |
| password | string | Yes | User password |

**Response:**
- **Success:** Redirect to `/home`
- **User Not Found:** Redirect to `/register` with info message
- **Invalid Password:** Render login page with error flash

**Session:**
- Session timeout: 5 minutes
- Session cookie is set on successful login

**Example:**
```html
<form method="POST" action="/login">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <button type="submit">Login</button>
</form>
```

---

### User Logout

End the current user session.

**Endpoint:** `GET /logout`

**Authentication Required:** Yes

**Response:**
- Redirect to `/login`

**Example:**
```html
<a href="/logout">Logout</a>
```

---

### Forgot Password

Initiate password recovery process.

**Endpoint:** 
- `GET /forgot_password` - Display form
- `POST /forgot_password` - Send OTP

**Request Type:** Form Data

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | User's email/username |

**External API Called:**
```
POST https://9l5xftepoj.execute-api.us-east-1.amazonaws.com/OTP/otp_verification
```

**Request Body:**
```json
{
    "path": "generate_otp",
    "userIdentifier": "user@example.com"
}
```

**Response:**
- Redirect to `/reset_password` with email parameter

---

### Reset Password

Complete password reset with OTP verification.

**Endpoint:**
- `GET /reset_password` - Display form
- `POST /reset_password` - Verify OTP and update password

**Request Type:** Form Data

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | User's email/username |
| otp | string | Yes | One-time password from email |
| new_password | string | Yes | New password to set |

**External API Called:**
```
POST https://9l5xftepoj.execute-api.us-east-1.amazonaws.com/OTP/otp_verification
```

**Request Body:**
```json
{
    "path": "verify_otp",
    "userIdentifier": "user@example.com",
    "otp": "123456"
}
```

**Response:**
- **Success:** Redirect to `/login`
- **Failure:** Redirect to `/login`

---

## Video Management

### Search Videos

Search for YouTube videos using keywords.

**Endpoint:** 
- `GET /search` - Display search page with default results
- `POST /search` - Search with custom keyword

**Request Type:** Form Data

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| keyword | string | No | Search keyword (default: "TRENDING") |

**External API Called:**
```
POST https://afyvb7t8u0.execute-api.us-east-1.amazonaws.com/prod/search_engine
```

**Request Body:**
```json
{
    "query": "Python tutorials"
}
```

**Response Format:**
```json
{
    "body": "[{\"title\": \"Video Title\", \"url\": \"https://youtube.com/watch?v=...\", \"description\": \"...\"}]"
}
```

**Template Variables:**
- `videos`: List of video objects
- `keyword`: Current search keyword

**Video Object Structure:**
```python
{
    "title": str,
    "url": str,  # Full YouTube URL
    "description": str
}
```

---

### Save Videos

Save selected videos to user's favorites.

**Endpoint:** `POST /save_videos`

**Authentication Required:** Yes

**Request Type:** Form Data

**Parameters:**
| Field | Type | Description |
|-------|------|-------------|
| video_ids[] | array | Array of video indices to save |
| title_{index} | string | Video title (hidden field) |
| url_{index} | string | Video URL (hidden field) |
| description_{index} | string | Video description (hidden field) |

**Example Form:**
```html
<form action="/save_videos" method="post">
    <input type="checkbox" name="video_ids[]" value="1">
    <input type="hidden" name="title_1" value="Video Title">
    <input type="hidden" name="url_1" value="https://youtube.com/...">
    <input type="hidden" name="description_1" value="Description">
    <button type="submit">Save Selected Videos</button>
</form>
```

**Response:**
- Redirect to `/search` with success/info flash message

**Flash Messages:**
- No selection: "No videos selected."
- Success: "Videos saved successfully!"
- Duplicates: "No new videos added. They might already exist."

**Database Action:**
- Creates `Video` records linked to `current_user.id`
- Prevents duplicate saves (same URL + user_id)

---

### View Saved Videos

Display all videos saved by the current user.

**Endpoint:** `GET /saved_videos`

**Authentication Required:** Yes

**Response:**
- Renders `saved_videos.html` template

**Template Variables:**
- `videos`: QuerySet of Video objects for current user

**Video Model:**
```python
{
    "id": int,
    "title": str,
    "url": str,
    "description": str,
    "user_id": int
}
```

---

### Delete Video

Remove a saved video from user's favorites.

**Endpoint:** `POST /delete_video/<video_id>`

**Authentication Required:** No (should be added)

**Parameters:**
| Field | Type | Description |
|-------|------|-------------|
| video_id | int | ID of video to delete (URL parameter) |

**Response:**
- Redirect to `/saved_videos` with info flash

**Flash Message:**
- "Video deleted successfully."

**Error Handling:**
- Returns 404 if video not found

---

## Article Search

### Search Articles

Search for news articles using NewsAPI.

**Endpoint:**
- `GET /articles` - Display default articles
- `POST /articles` - Search with custom keyword

**Request Type:** Form Data

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| keyword | string | No | Search keyword (default: "expense management") |

**External API Called:**
```
GET https://newsapi.org/v2/everything
```

**Query Parameters:**
```
q: keyword
language: en
apiKey: {NEWS_API_KEY from .env}
```

**Response Format:**
```json
{
    "articles": [
        {
            "title": "Article Title",
            "description": "...",
            "url": "https://...",
            "urlToImage": "https://...",
            "publishedAt": "2024-01-01T00:00:00Z",
            "source": {"name": "Source Name"}
        }
    ]
}
```

**Template Variables:**
- `articles`: List of article objects
- `keyword`: Current search keyword

---

## Static Pages

### Home Page

**Endpoint:** `GET /`

**Template:** `home.html`

**Description:** Landing page with feature overview

---

### About Page

**Endpoint:** `GET /about`

**Template:** `about.html`

**Description:** Information about the application

---

### Contact Page

**Endpoint:** `GET /contact`

**Template:** `contact.html`

**Description:** Contact form for user inquiries

---

### Handle Contact Form

**Endpoint:** `POST /handle_contact_form`

**Request Type:** Form Data

**Parameters:**
| Field | Type | Required |
|-------|------|----------|
| name | string | Yes |
| email | string | Yes |
| message | text | Yes |

**Response:**
- Redirect to `/contact` with success flash

**Flash Message:**
- "Thank you for your message, we will be in touch soon!"

**Note:** Currently doesn't persist data; needs implementation.

---

## Request/Response Examples

### Example 1: Complete User Registration Flow

**1. Register:**
```bash
curl -X POST http://localhost:5000/register \
  -F "username=john@example.com" \
  -F "password=SecurePass123"
```

**2. Login:**
```bash
curl -X POST http://localhost:5000/login \
  -F "username=john@example.com" \
  -F "password=SecurePass123" \
  -c cookies.txt
```

**3. Search Videos:**
```bash
curl -X POST http://localhost:5000/search \
  -F "keyword=Python tutorials" \
  -b cookies.txt
```

### Example 2: Video Search and Save

**Python Example:**
```python
import requests

# Create session
session = requests.Session()

# Login
login_data = {
    'username': 'john@example.com',
    'password': 'SecurePass123'
}
session.post('http://localhost:5000/login', data=login_data)

# Search videos
search_data = {'keyword': 'Flask tutorials'}
response = session.post('http://localhost:5000/search', data=search_data)

# Save videos (requires form data matching template structure)
save_data = {
    'video_ids[]': ['1', '2'],
    'title_1': 'Flask Tutorial Part 1',
    'url_1': 'https://youtube.com/watch?v=abc123',
    'description_1': 'Introduction to Flask',
    'title_2': 'Flask Tutorial Part 2',
    'url_2': 'https://youtube.com/watch?v=def456',
    'description_2': 'Advanced Flask'
}
session.post('http://localhost:5000/save_videos', data=save_data)
```

---

## Database Models

### User Model

```python
class User(UserMixin, db.Model):
    id: int (Primary Key)
    username: str (Unique, Not Null, max 100 chars)
    password: str (Hashed, Not Null, max 100 chars)
```

### Video Model

```python
class Video(db.Model):
    id: int (Primary Key)
    title: str (Not Null, max 255 chars)
    url: str (Not Null, max 512 chars)
    description: text (Nullable)
    user_id: int (Foreign Key -> User.id, Not Null)
    user: relationship to User
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 302 | Redirect (after form submission) |
| 404 | Resource not found (e.g., video_id) |
| 500 | Internal server error |

---

## Rate Limits

### NewsAPI
- **Free Tier:** 100 requests per day
- **Response:** 429 Too Many Requests (if exceeded)

### AWS Endpoints
- Rate limits depend on AWS API Gateway configuration
- Contact API administrator for details

---

## Authentication Notes

- **Session Timeout:** 5 minutes of inactivity
- **Password Hashing:** Werkzeug PBKDF2 SHA-256
- **Login Required Routes:**
  - `/save_videos`
  - `/saved_videos`
  - `/logout`

---

## Security Considerations

1. **HTTPS:** Use HTTPS in production
2. **Environment Variables:** Never commit `.env` file
3. **SQL Injection:** Protected by SQLAlchemy ORM
4. **XSS:** Flask auto-escapes template variables
5. **CSRF:** Consider adding Flask-WTF for CSRF tokens

---

For setup instructions, see [SETUP.md](SETUP.md).  
For general information, see [README.md](README.md).
