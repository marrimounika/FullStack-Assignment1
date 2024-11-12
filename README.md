# FullStack-Assignment1

# *BookExchangePlatform*

BookExchange is a web application that allows users to manage books, exchange requests, and messages. Users can create profiles, list books for exchange, and communicate with other users seamlessly.

---

## *Features*

- *User Authentication*
  - Registration and login using Flask-Login.
  - Password reset functionality.
  
- *Profile Management*
  - Update user profile with reading preferences, favorite genres, and profile pictures.
  - Password change functionality.

- *Book Management*
  - Add, edit, and delete books with optional cover images.
  - List all books owned by the user.
  
- *Exchange Requests*
  - Send and manage book exchange requests.
  - Accept or reject incoming exchange requests.
  
- *Messaging*
  - Message other users to discuss book exchanges.
  - View message history and manage conversations.

---

## *Tech Stack*

- *Backend:*
  - Python, Flask
  - Flask-SQLAlchemy for ORM
  - Flask-WTF for form handling
  - Flask-Login for authentication
  - Flask-Migrate for database migrations

- *Frontend:*
  - HTML, CSS, Jinja2 templating
  - Bootstrap for responsive UI

- *Database:*
  - SQLite (can be replaced with PostgreSQL or MySQL)

---

## *Setup Instructions*

### Prerequisites

1. Python (3.8 or later)
2. pip (Python package installer)
3. Virtual environment (recommended)

### Installation

1. *Clone the repository:*

   ```
   git clone https://github.com/marrimounika/FullStack-Assignment1/tree/main
   cd bookexchange
   ```

2. *Set up a virtual environment:*

   ```
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. *Install dependencies:*

   ```
   pip install -r requirements.txt
   ```

4. *Set up environment variables:*

   Create a .env file in the root directory and configure the following:
   env
   ```
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=sqlite:///app.db
   FLASK_ENV=development
   UPLOAD_FOLDER=static/uploads
   ```

6. *Run database migrations:*

   ```
   flask db upgrade
   ```

7. *Run the application:*

   ```
   flask run
   ```

8. *Access the application:*

   Open your browser and go to http://127.0.0.1:5000.

---

## *Project Structure*
```
plaintext
bookexchange/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # Database models
│   ├── forms.py             # WTForms definitions
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   ├── books.py         # Book management routes
│   │   ├── profile.py       # User profile routes
│   │   ├── exchanges.py     # Exchange management routes
│   │   └── messages.py      # Messaging routes
│   ├── templates/           # HTML templates
│   └── static/              # Static files (CSS, JS, images)
├── migrations/              # Flask-Migrate files
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── config.py                # Configuration settings
├── README.md                # Project README
└── run.py                   # Entry point to run the app
```

---

## *Contributing*

1. Fork the repository.
2. Create a feature branch:
   bash
   git checkout -b feature-name
   
3. Commit changes:
   bash
   git commit -m "Add a descriptive commit message"
   
4. Push to the branch:
   bash
   git push origin feature-name
   
5. Open a pull request.

---

## *License*

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## *Acknowledgments*

- Flask documentation
- Bootstrap for responsive design
- SQLAlchemy for database ORM
