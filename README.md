# Nishanth Ganji's Personal Website - Flask Version

This is a Flask-based personal website that maintains the exact same look and feel as the original HTML version, now enhanced with database functionality for dynamic content management.

## Features

- **Responsive Design**: Modern, clean interface that works on all devices
- **Dynamic Navigation**: Active page highlighting and mobile-friendly navigation
- **Contact Form**: Functional contact form with client-side validation and database storage
- **Project Management**: Dynamic project listing with ability to add new projects
- **Database Integration**: SQLite databases for projects and contact form submissions
- **Interactive Elements**: Smooth animations and dynamic background gradients
- **Professional Content**: Portfolio showcasing education, experience, and projects

## Installation and Setup

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask Application**:
   ```bash
   python app.py
   ```

3. **Access the Website**:
   Open your browser and go to `http://localhost:5000`

## Project Structure

```
├── app.py                 # Main Flask application
├── DAL.py                 # Data Access Layer for projects
├── contact_DAL.py         # Data Access Layer for contacts
├── projects.db            # SQLite database for projects
├── contacts.db            # SQLite database for contact submissions
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── about.html        # About page
│   ├── resume.html       # Resume page
│   ├── projects.html     # Projects page
│   ├── project_form.html # Add new project form
│   ├── contact.html      # Contact page
│   └── thankyou.html     # Thank you page
└── static/               # Static assets
    ├── css/
    │   └── styles.css    # Main stylesheet
    ├── js/
    │   ├── scripts.js    # Main JavaScript
    │   ├── ui.js         # UI utilities
    │   └── shapes.js     # Shape animations
    └── images/           # All images
```

## Pages

- **Home** (`/`): Landing page with hero section and profile
- **About** (`/about`): Personal background and interests
- **Resume** (`/resume`): Professional experience and education
- **Projects** (`/projects`): Dynamic project listing from database
- **Add Project** (`/projects/new`): Form to add new projects to the database
- **Contact** (`/contact`): Contact information and form with database storage
- **Thank You** (`/thank-you`): Form submission confirmation

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite with custom Data Access Layer (DAL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Templates**: Jinja2 templating engine
- **Icons**: Emoji icons for visual appeal

## Contact Form

The contact form includes:
- Client-side validation for all fields
- Password confirmation validation
- Email format validation
- Server-side processing with Flask
- Database storage of form submissions
- Flash messaging for user feedback

## Database Functionality

The application uses two SQLite databases:

### Projects Database (`projects.db`)
- **Table**: `projects` with fields: id, Title, Description, ImageFileName, CreatedAt
- **Features**: 
  - Automatic database initialization with seed data
  - Dynamic project listing on the projects page
  - Add new projects via web form
  - Pre-populated with sample projects

### Contacts Database (`contacts.db`)
- **Table**: `contacts` with fields: id, first_name, last_name, email, password, created_at
- **Features**:
  - Stores contact form submissions
  - Automatic timestamping of submissions
  - Data validation before storage

### Data Access Layer (DAL)
- **`DAL.py`**: Handles project database operations
- **`contact_DAL.py`**: Handles contact form database operations
- Both modules provide clean separation between database logic and application logic

## Project Management

The website includes a project management system:
- **View Projects**: Dynamic listing of all projects from the database
- **Add Projects**: Web form to add new projects with validation
- **Project Form**: Includes fields for title, description, and image filename
- **Image Management**: Projects reference image files stored in `/static/images/`

## Development

To run in development mode:
```bash
export FLASK_ENV=development
python app.py
```

This enables debug mode with auto-reload for development.

## Deployment

For production deployment, consider using:
- Gunicorn as WSGI server
- Nginx as reverse proxy
- Environment variables for configuration
- Proper secret key management
