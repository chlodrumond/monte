# Monte Academic Platform

A comprehensive academic platform built with Django, designed to provide PUC-Rio students with an integrated learning experience featuring mountain-themed gamification.

## Features

- **User Authentication**: Signup/login with @aluno.puc-rio.br email validation
- **Material Upload**: Share academic materials with altitude rewards (50m per upload)
- **Search & Filter**: Advanced search by type, subject, period, keywords, and tags
- **Comments & Ratings**: Interactive feedback system with altitude rewards
- **Mountain Progression**: 9-level gamification system starting at Sea Level
- **User Profiles**: Personal dashboard showing progress and mountain conquests
- **Ranking System**: Community leaderboard based on altitude achievements
- **Favorites System**: Users can save materials for later access
- **Social Sharing**: Share materials via WhatsApp, Twitter, Facebook, or Email
- **Content Curation**: Featured materials and popularity-based rankings
- **Enhanced Admin**: Full administrative control with content moderation
- **Responsive Design**: Mobile-first design with navy blue/gold branding

## Technology Stack

- **Backend**: Django 5.2 with Python
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend**: Bootstrap 5.3.0, Font Awesome 6.4.0, Google Fonts
- **Forms**: Django Crispy Forms with Bootstrap 5 styling
- **Authentication**: Custom user authentication with email validation

## Mountain Progression System

The platform features a unique gamification system where users progress through mountain levels:

1. **Sea Level** (0-49m) - Starting point for new users
2. **Pedra Bonita** (50-149m) - First mountain achievement
3. **Pico da Tijuca** (50-149m)
4. **Corcovado** (50-149m)
5. **Machu Picchu** (150-299m)
6. **Pedra da Gávea** (150-299m)
7. **Monte Roraima** (300-499m)
8. **Kilimanjaro** (500-799m)
9. **Pico dos Marins** (500-799m)
10. **Monte Fuji** (800-1199m)
11. **Pico das Agulhas Negras** (800-1199m)
12. **Mont Blanc** (1200-1999m)
13. **Everest** (2000m+) - Ultimate achievement

## Setup Instructions

### Prerequisites

- Python 3.11+
- pip
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/monte-platform.git
cd monte-platform
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Collect static files:
```bash
python manage.py collectstatic
```

8. Run the development server:
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the platform.

## Environment Variables

Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ADMIN_EMAIL=your-admin@aluno.puc-rio.br
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

For production, set appropriate values for:
- `DEBUG=False`
- `SECRET_KEY` (generate a secure key)
- `DATABASE_URL` (PostgreSQL connection string)
- Email configuration for SMTP

## Deployment

### Heroku Deployment

1. Install Heroku CLI
2. Create Heroku app:
```bash
heroku create your-app-name
```

3. Add PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ADMIN_EMAIL=your-admin@aluno.puc-rio.br
```

5. Deploy:
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## Project Structure

```
monte-platform/
├── core/                   # Core Django settings and utilities
├── materials/              # Main app for materials and user management
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin configuration
│   └── urls.py            # URL patterns
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Landing page
│   └── materials/         # App-specific templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
├── monte_platform/         # Django project settings
└── manage.py              # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, contact the development team or create an issue in this repository.