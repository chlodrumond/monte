# Monte Academic Platform

## Overview

Monte Academic Platform is a Flask-based web application designed as an academic platform with a mountaineering metaphor. The application features a minimalist design with a navy blue and gold color scheme, providing users with a homepage and login functionality. The platform is built using Flask as the backend framework with Bootstrap and custom CSS for the frontend.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Application Structure**: Simple monolithic structure with a single `app.py` file containing all routes
- **Session Management**: Uses Flask's built-in session handling with a configurable secret key
- **Proxy Support**: Configured with ProxyFix middleware for deployment behind reverse proxies

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default templating engine)
- **CSS Framework**: Bootstrap 5.3.0 for responsive design and components
- **Icon Library**: Font Awesome 6.4.0 for icons
- **Typography**: Google Fonts (Crimson Text) for serif typography
- **JavaScript**: Vanilla JavaScript for interactive components (hamburger menu)

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

## Future Development Areas

1. **Database Integration**: Ready for database implementation (likely PostgreSQL with potential Drizzle ORM integration)
2. **Authentication System**: Foundation exists for implementing proper user authentication
3. **User Management**: Session handling infrastructure ready for user state management
4. **API Development**: Flask structure supports REST API development
5. **Content Management**: Academic platform features can be built on existing foundation