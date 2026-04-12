# CIThai – AI-Powered Music Generation Platform

A web-based AI music generation platform that enables users to create personalized songs based on occasion, genre, mood, and custom lyrics.

---

## Tech Stack

- Python 3.13
- Django 5.2
- Django REST Framework
- SQLite (development)

---

## Project Structure

```
CIThai/
├── cithai/                  # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── music/                   # Main application
│   ├── models/              # One file per domain class
│   │   ├── __init__.py
│   │   ├── enums.py         # GenerationStatus, Mood, Genre, Occasion, VoiceType
│   │   ├── user.py          # User model
│   │   ├── song.py          # Song model
│   │   ├── song_generation.py  # SongGeneration model
│   │   └── share_link.py    # ShareLink model
│   ├── views/
│   │   ├── __init__.py
│   │   ├── song_views.py    # SongViewSet, SongGenerationViewSet
│   │   └── share_views.py   # ShareLinkViewSet
│   ├── migrations/
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── manage.py
└── requirements.txt
```

---

## Setup

```
# 1. Clone the repository
git clone https://github.com/fcxbsyo/CIThai.git
cd CIThai

# 2. Create and activate virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

---

## Song Generation (Strategy Pattern)

The system supports two interchangeable song generation strategies controlled by the `GENERATOR_STRATEGY` environment variable.

### Mock Mode (default)

Mock mode runs offline with no external API calls. It returns a fixed placeholder audio URL and is used for development and testing.

Create a `.env` file in the project root:

```
GENERATOR_STRATEGY=mock
```

To verify mock generation works:

```
python3 manage.py demo_generation --strategy mock
```

Expected output: `final status : mock_complete`

### Suno Mode (real AI generation)

Suno mode calls the [SunoAPI.org](https://sunoapi.org) external service to generate real songs.

Add the following to your `.env` file:

```
GENERATOR_STRATEGY=suno
SUNO_API_KEY=your_api_key_here
```

To verify Suno generation works:

```
python3 manage.py demo_generation --strategy suno
```

Expected output: a real `task_id` returned from SunoAPI, followed by status polling until complete.

### API Key Security

- The Suno API key is read from the `SUNO_API_KEY` environment variable
- **Never hardcode the key in source code or commit it to Git**
- `.env` is already listed in `.gitignore` — keep it that way
- Get your API key from [https://sunoapi.org](https://sunoapi.org)

---

## API Endpoints

| Method                  | Endpoint                 | Description                              |
| ----------------------- | ------------------------ | ---------------------------------------- |
| GET, POST               | `/api/songs/`            | List all songs / Create song             |
| GET, PUT, PATCH, DELETE | `/api/songs/{id}/`       | Retrieve / Update / Delete song          |
| GET, POST               | `/api/generations/`      | List all generations / Create generation |
| GET, PUT, PATCH, DELETE | `/api/generations/{id}/` | Retrieve / Update / Delete generation    |
| GET, POST               | `/api/sharelinks/`       | List all share links / Create share link |
| GET, PUT, PATCH, DELETE | `/api/sharelinks/{id}/`  | Retrieve / Update / Delete share link    |
| GET, POST               | `/api/genres/`           | List all genres / Create genre           |
| GET, PUT, PATCH, DELETE | `/api/genres/{id}/`      | Retrieve / Update / Delete genre         |
| GET, POST               | `/api/occasions/`        | List all occasions / Create occasion     |
| GET, PUT, PATCH, DELETE | `/api/occasions/{id}/`   | Retrieve / Update / Delete occasion      |

Browse the full API at: `http://127.0.0.1:8000/api/`

---

## CRUD Demo Screenshots

[View CRUD screenshots](CRUD)

---

## Admin

Manage all data at: `http://127.0.0.1:8000/admin/`

Models registered:

- User
- Song
- SongGeneration
- ShareLink

---

## Domain Model

<img src="domain_model.png" alt="Domain Model" width="700"/>

Core business entities:

- **User** — registered person who owns and shares songs
- **Song** — completed AI-generated creative work
- **SongGeneration** — business record of a generation attempt
- **ShareLink** — controlled sharing permission attached to a song
