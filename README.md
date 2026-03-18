# Cithai

## Requirements

- Python 3.x
- Django 4.x

## Setup

1. Clone the repository
   ```
   git clone <https://github.com/fcxbsyo/CIThai>
   cd cithai
   ```

2. Create and activate virtual environment
   ```
   python -m venv venv
   source venv/bin/activate # Mac/Linux
   venv\Scripts\activate # Windows
   ```

3. Install dependencies
   ```
   pip install django
   ```

4. Apply migrations
   ```
   python manage.py migrate
   ```

5. Run the server
   ```
   python manage.py runserver
   ```

## Project Structure
```
cithai/
├── cithai/ # Django project settings
├── music/ # Domain app
│ ├── models.py # Domain entities
│ ├── admin.py # CRUD via Django Admin
│ └── migrations/ # Database migrations
├── manage.py
└── requirements.txt
```
## Domain Model

![Domain Model](domain_model.png)
