# The Cakery

## Prerequisites

- Python 3.12
- Django 5.0
- SQLite
- Git

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chhay-sophal/the-cakery.git
   cd the-cakery
   ```

2. **Create and activate virtual environement**:
   ```bash
   python -m venv env
   # Windows (cmd)
   venv\Scripts\activate
   # Windows (Git Bash)
   source env/scripts/activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install the required dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Migrate Database**:
   ```
   python manage.py migrate
   ```

5. **Create a superuser for accessing the Django admin**:
   ```
   python manage.py createsuperuser
   ```

6. **Collect static files**:
   ```
   python manage.py collectstatic
   ```

## Run the Application

1. **Start the development server**:
   ```
   python manage.py runserver
   ```

2. Open your web browser and visit http://127.0.0.1:8000/ to access the application.

