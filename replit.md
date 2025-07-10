# Monte Academic Platform

## Overview

Monte Academic Platform is a complete Django-based educational platform with a mountain-themed gamification system. Students can upload and share academic materials, earn altitude points, and progress through mountain levels from Pedra Bonita to Everest. The platform features PUC-Rio email validation, user authentication, material sharing, commenting, rating systems, and user rankings. The application uses a navy blue and gold color scheme with responsive design.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Django 5.2 (Python web framework)
- **Application Structure**: Full Django project with `monte_platform` main project and `materials` app
- **Database**: SQLite with Django ORM models for users, materials, comments, ratings, and gamification
- **Authentication**: Custom user authentication with @puc-rio.br email validation
- **Gamification**: Mountain-based progression system with altitude points and achievements

### Frontend Architecture
- **Template Engine**: Django templates with template inheritance
- **CSS Framework**: Bootstrap 5.3.0 for responsive design and components
- **Forms**: Django Crispy Forms with Bootstrap 5 styling
- **Icon Library**: Font Awesome 6.4.0 for icons
- **Typography**: Google Fonts (Crimson Text) for serif typography
- **JavaScript**: Vanilla JavaScript for interactive components (hamburger menu, dynamic forms)

### Design System
- **Color Palette**: Navy blue (#0B1C2D) and gold (#CEB974) for brand consistency
- **Typography**: Crimson Text serif font for elegant, academic appearance
- **Layout**: Responsive design with mobile-first approach
- **UI Components**: Custom offcanvas menu, flash message system, split-screen login layout

## Key Components

### 1. Application Entry Point (`app.py`)
- Flask application initialization with security configurations
- Route definitions for homepage and login functionality
- Flash messaging system for user feedback
- Basic form validation for login attempts

### 2. Template System
- **Homepage (`templates/index.html`)**: Features centered logo, descriptive text, and hamburger menu
- **Login Page (`templates/login.html`)**: Split-screen design with logo on left, form on right
- Both templates include responsive design and accessibility features

### 3. Static Assets
- **CSS (`static/css/style.css`)**: Custom styling with CSS variables for theme consistency
- **JavaScript (`static/js/script.js`)**: Menu functionality and form validation
- **Images**: Logo storage in `static/img/` directory

### 4. User Interface Features
- Hamburger menu with offcanvas sidebar navigation
- Flash message system for user notifications
- Responsive form layouts with proper validation feedback
- Accessibility considerations (ARIA labels, keyboard navigation)

## Data Flow

### Current Implementation
1. **Homepage Access**: User visits root URL → Flask renders `index.html` template
2. **Menu Interaction**: User clicks hamburger menu → JavaScript toggles offcanvas menu
3. **Login Access**: User clicks "Acessar" → Redirects to `/login` route
4. **Form Submission**: User submits login form → Flask processes POST request → Validates input → Shows flash message → Redirects to homepage

### Authentication Flow (Current Demo)
- Basic form validation (presence of email and password)
- Flash message confirmation for demo purposes
- No actual authentication or session management implemented
- Ready for integration with proper authentication system

## External Dependencies

### Frontend Dependencies (CDN)
- **Bootstrap 5.3.0**: UI framework for responsive components
- **Font Awesome 6.4.0**: Icon library for UI elements
- **Google Fonts**: Crimson Text font family for typography

### Python Dependencies
- **Flask**: Web framework for routing and templating
- **Werkzeug**: WSGI utilities (ProxyFix middleware)

### Development Tools
- Debug mode enabled for development
- Hot reloading configured
- Environment variable support for configuration

## Deployment Strategy

### Current Configuration
- **Host**: Configured to run on `0.0.0.0` for container compatibility
- **Port**: Default port 5000
- **Debug Mode**: Enabled for development (should be disabled in production)
- **Proxy Support**: ProxyFix middleware configured for reverse proxy deployment

### Environment Variables
- `SESSION_SECRET`: Configurable secret key for session security
- Falls back to default value if not provided

### Scalability Considerations
- Single-file application structure is suitable for small applications
- Ready for modularization as the application grows
- Static file serving configured for development (production should use CDN or reverse proxy)

### Security Features
- CSRF protection ready for implementation
- Session security with configurable secret key
- Form validation foundation in place
- Accessibility features implemented (ARIA labels, keyboard navigation)

## Recent Changes (July 2025)

1. **Complete Django Migration**: Migrated from Flask prototype to full Django application
2. **User Authentication**: Implemented custom signup/login with @puc-rio.br email validation
3. **Gamification System**: Built mountain progression with 8 levels (Pedra Bonita to Everest)
4. **Material Management**: Upload, search, comment, and rating system for academic materials
5. **User Interface**: Complete responsive UI with user profiles, rankings, and notifications
6. **Logo Update**: Integrated new logo provided by user (July 10, 2025)
7. **Admin Panel**: Configured Django admin with sample data for testing

## Current Features

- **User Authentication**: Signup/login with PUC-Rio email validation
- **Material Upload**: Share academic materials with altitude rewards (50m per upload)
- **Search & Filter**: Advanced search by type, subject, period, and keywords
- **Comments & Ratings**: Interactive feedback system with altitude rewards
- **Mountain Progression**: 8-level gamification system with achievement tracking
- **User Profiles**: Personal dashboard showing progress and mountain conquests
- **Ranking System**: Community leaderboard based on altitude achievements
- **Responsive Design**: Mobile-first design with navy blue/gold branding