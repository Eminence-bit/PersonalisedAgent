# Personalized AI Agent

A powerful AI assistant that helps users manage their tasks, calendar events, and provides smart suggestions based on their schedule. This application connects with Google services to provide a seamless productivity experience.

## Features

- **Google Calendar Integration**: View and manage your calendar events
- **Smart Task Suggestions**: Receive AI-powered suggestions based on your events
- **Beautiful Modern UI**: Enjoy a responsive and intuitive user interface
- **Secure Authentication**: Uses OAuth 2.0 for secure Google account access

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Google API credentials (client_secret.json)
- A modern web browser

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/PersonalisedAgent.git
cd PersonalisedAgent
```

2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables by creating a `.env` file in the root directory:

```
FLASK_SECRET_KEY=your_generated_secret_key
```

You can generate a secure key using the provided script:

```bash
python generate_secret.py
```

5. Place your `client_secret.json` file (from Google Cloud Console) in the project root

### Running the Application

Start the Flask development server:

```bash
python app.py
```

Access the application at: http://127.0.0.1:5000

## Project Structure

- `app.py` - Main Flask application file
- `google_calendar.py` - Google Calendar API integration
- `task_predictor.py` - ML model for task prediction
- `templates/` - HTML templates for the UI
  - `landing.html` - Landing page
  - `dashboard.html` - User dashboard
- `.env` - Environment variables (not in version control)
- `requirements.txt` - Python dependencies

## Security Notes

- The `.env` file containing your secret key should never be committed to version control
- For production deployment, set environment variables directly on your server
- Client secrets and tokens are excluded from version control via `.gitignore`

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML, CSS, Bootstrap 5
- **Authentication**: Google OAuth 2.0
- **API Integration**: Google Calendar API, Google People API
- **UI Enhancements**: AOS animations, Chart.js

## License

This project is licensed under the MIT License - see the LICENSE file for details.
