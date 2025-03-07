# Grabify - Book Review Community

Grabify is a modern book review platform where users can share their reading experiences, discover new books, and connect with fellow book enthusiasts.

## Features

- User Authentication (Register, Login, Logout)
- Create, Read, Update, and Delete Book Reviews
- Book Cover Image Upload
- Reading Status Tracking (Currently Reading, Finished, Want to Read, DNF)
- Genre-based Categorization
- Search and Filter Reviews
- Responsive Design
- Social Sharing

## Tech Stack

- Django 4.2.7
- Bootstrap 5
- Font Awesome 5
- SQLite (Development) / PostgreSQL (Production)
- Pillow for Image Processing
- Crispy Forms for Form Rendering
- Whitenoise for Static Files
- Gunicorn for Production Server

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/grabify.git
cd grabify
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add:
```
SECRET_KEY=your_secret_key
DEBUG=True
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

Visit http://localhost:8000 to see the application.

## Deployment

The application is deployed on Firebase Cloud Run. To deploy:

1. Install Firebase CLI:
```bash
npm install -g firebase-tools
```

2. Login to Firebase:
```bash
firebase login
```

3. Initialize Firebase:
```bash
firebase init
```

4. Deploy:
```bash
firebase deploy
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors who have helped shape Grabify
- Built with ❤️ for book lovers everywhere 