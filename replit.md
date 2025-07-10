# Monte Academic Platform

## Overview

Monte Academic Platform is a comprehensive Django-based educational collaborative platform designed with a mountaineering metaphor. The application features a complete academic sharing system with user authentication, file uploads, rating system, and gamification through altitude points. Users can share educational materials, rate content, and climb virtual mountains based on their contributions to the academic community.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Django 5.2.4 (Python web framework)
- **Application Structure**: Modular Django structure with `core` app containing all functionality
- **Database**: SQLite (default Django ORM with custom models)
- **Authentication**: Django's built-in authentication system with custom UserProfile extension
- **File Management**: Django FileField with custom upload paths and validation
- **Session Management**: Django's session framework with database backend

### Frontend Architecture
- **Template Engine**: Django Templates with template inheritance
- **CSS Framework**: Bootstrap 5.3.0 for responsive design and components
- **Form Processing**: Django Forms with crispy-forms for enhanced styling
- **Icon Library**: Font Awesome 6.4.0 for icons
- **Typography**: Google Fonts (Crimson Text) for serif typography
- **JavaScript**: Vanilla JavaScript for interactive components and form validation

### Design System
- **Color Palette**: Navy blue (#0B1C2D) and gold (#CEB974) for brand consistency
- **Typography**: Crimson Text serif font for elegant, academic appearance
- **Layout**: Responsive design with mobile-first approach
- **UI Components**: Custom offcanvas menu, flash message system, split-screen login layout

## Key Components

### 1. Django Models (`core/models.py`)
- **UserProfile**: Extended user information with altitude points and course
- **Material**: Educational content with file uploads, metadata, and download tracking
- **Avaliacao**: User ratings for materials with 1-5 star system
- **Comentario**: User comments on materials
- **Signal Handlers**: Automatic point assignment for user actions

### 2. Views and URL Routing (`core/views.py`, `core/urls.py`)
- **Authentication Views**: Custom signup with PUC-Rio email validation
- **Material Management**: Upload, search, detail views with pagination
- **User Profile**: Personal dashboard with activity tracking
- **Ranking System**: Leaderboard based on altitude points

### 3. Template System
- **Base Template**: Common layout with navigation and messaging
- **Homepage**: Welcome page with user progress display
- **Authentication Pages**: Login and signup with validation
- **Material Pages**: Upload forms, search results, detailed material view
- **User Dashboard**: Profile management and activity overview

### 4. Form Processing (`core/forms.py`)
- **Custom User Creation**: Validates PUC-Rio email domain
- **Material Upload**: File validation and metadata collection
- **Search and Filter**: Advanced material discovery
- **User Profile Management**: Account information updates

### 5. Gamification System
- **Mountain Progression**: Users advance through mountains based on points
- **Point System**: Upload (50), Comment (10), Receive Rating (5)
- **Ranking Display**: Competitive leaderboard with podium visualization

## Data Flow

### Complete Implementation
1. **Homepage Access**: User visits root URL → Django renders homepage with user context
2. **Authentication Flow**: 
   - Signup: Validates PUC-Rio email → Creates user and profile → Auto-login
   - Login: Django authentication → Redirects to user profile
3. **Material Management**:
   - Upload: File validation → Saves to user directory → Adds 50 altitude points
   - Search: Query processing → Filtered results with pagination → Average ratings
   - Detail View: Material info → Comments and ratings → Download tracking
4. **Gamification**:
   - Point accumulation through user actions
   - Mountain progression based on altitude points
   - Ranking updates automatically through Django signals

### User Journey
- New users register with PUC-Rio email and start at "Morro da Urca"
- Contributing materials and engaging with content earns altitude points
- Users progress through mountains: Urca → Pão de Açúcar → Pedra da Gávea → Pico da Neblina → Kilimanjaro → Everest
- Social features encourage collaboration through comments and ratings

## External Dependencies

### Frontend Dependencies (CDN)
- **Bootstrap 5.3.0**: UI framework for responsive components
- **Font Awesome 6.4.0**: Icon library for UI elements
- **Google Fonts**: Crimson Text font family for typography

### Python Dependencies
- **Django 5.2.4**: Web framework with ORM, authentication, and templating
- **django-crispy-forms**: Enhanced form styling with Bootstrap integration
- **crispy-bootstrap5**: Bootstrap 5 support for crispy forms
- **Pillow**: Image processing for file upload validation

### Development Tools
- Debug mode enabled for development
- Hot reloading configured
- Environment variable support for configuration

## Deployment Strategy

### Current Configuration
- **WSGI Application**: Django WSGI with Gunicorn server
- **Host**: Configured to run on `0.0.0.0:5000` for container compatibility
- **Debug Mode**: Enabled for development (should be disabled in production)
- **Static Files**: Collected and served through Django's static file system
- **Media Files**: User uploads stored in `media/` directory with organized subdirectories

### Environment Variables
- Django secret key management
- Database configuration (currently SQLite for development)
- Media and static file paths configured

### Scalability Considerations
- Modular Django architecture supports horizontal scaling
- Database can be migrated to PostgreSQL for production
- Static and media files ready for CDN deployment
- Signal-based point system scales with user activity

### Security Features
- **CSRF Protection**: Django's built-in CSRF middleware active
- **User Authentication**: Secure login/logout with session management
- **File Upload Validation**: Restricted file types and size limits (10MB max)
- **Email Domain Validation**: Only @puc-rio.br emails accepted
- **Input Sanitization**: Django's automatic SQL injection and XSS protection
- **Access Control**: Login required for uploading, commenting, and downloading

## Completed Features

1. **✅ User Authentication**: Complete signup/login system with PUC-Rio email validation
2. **✅ File Management**: Material upload with PDF/DOC support and download tracking
3. **✅ Search System**: Advanced filtering by type, subject, and keyword search
4. **✅ Rating System**: 5-star ratings with comments for all materials
5. **✅ Gamification**: Mountain-based progression with altitude points
6. **✅ User Profiles**: Personal dashboards with activity tracking
7. **✅ Ranking System**: Competitive leaderboard with podium display
8. **✅ Responsive Design**: Mobile-friendly interface with Bootstrap integration

## Recent Changes (January 2025)

- **🔄 Framework Migration**: Converted from Flask to Django for enhanced functionality
- **➕ Database Models**: Implemented comprehensive data structure with relationships
- **➕ Authentication System**: Added complete user management with profile extension
- **➕ File Upload System**: Secure file handling with validation and organized storage
- **➕ Gamification**: Introduced mountain-based point system with automatic progression
- **➕ Social Features**: Added commenting and rating system for community engagement