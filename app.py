from flask import Flask, render_template, redirect, url_for, session, request
from task_predictor import TaskPredictor
from google_calendar import fetch_events
from datetime import datetime
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from googleapiclient.discovery import build
import os
import json

import secrets
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)
# Use secret key from environment variable, or generate a secure one if not available
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or secrets.token_hex(32)

# If we generated a new key, log a warning
if 'FLASK_SECRET_KEY' not in os.environ:
    print("WARNING: Using a temporary secret key. Set FLASK_SECRET_KEY environment variable for consistent sessions.")

predictor = TaskPredictor()

# Google OAuth configuration
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'openid']

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Get the authorization response URL
    authorization_response = request.url
    
    # Create a flow instance with the client secrets and scopes
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/calendar.readonly',
                'openid'],  # Add 'openid' to the scopes
        redirect_uri=url_for('oauth2callback', _external=True)
    )
      # Use the flow to fetch the token
    flow.fetch_token(authorization_response=authorization_response)
    
    # Store the credentials in the session
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    # Get user info from people API directly instead of ID token
    try:
        # Build the people API service
        people_service = build('people', 'v1', credentials=credentials)
        
        # Get the user's profile from the people API
        profile = people_service.people().get(
            resourceName='people/me',
            personFields='names,emailAddresses,photos'
        ).execute()
        
        # Extract user info
        name = profile.get('names', [{}])[0].get('displayName', 'User')
        email = profile.get('emailAddresses', [{}])[0].get('value', 'user@example.com')
        picture = profile.get('photos', [{}])[0].get('url', None)
        
        # Store user info in session
        session['user'] = {
            'email': email,
            'name': name,
            'picture': picture
        }
    except Exception as e:
        # If API call fails, create a basic user session
        print(f"Error getting user profile: {str(e)}")
        session['user'] = {
            'email': 'user@example.com',
            'name': 'User',
            'picture': None
        }
    
    # Redirect to the dashboard page
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        # Fetch calendar events
        events = fetch_events()
        suggestions = []
    except Exception as e:
        # Handle any errors during calendar fetching
        print(f"Error fetching calendar events: {str(e)}")
        events = []
        suggestions = []
    
    for event in events:
        summary = event.get('summary', '')
        start_time = event.get('start', {}).get('dateTime', '')
        if start_time:
            # Convert ISO format to readable time
            time = datetime.fromisoformat(start_time.replace('Z', '+00:00')).strftime('%I:%M %p')
        else:
            time = 'All day'
            
        suggestion = predictor.predict(summary)
        suggestions.append({
            'event': summary,
            'time': time,
            'suggestion': suggestion
        })
    
    # Get current date in a nice format
    current_date = datetime.now().strftime('%A, %B %d, %Y')
    
    return render_template('dashboard.html', 
                         suggestions=suggestions,
                         current_date=current_date,
                         user=session['user'])

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Remove in production
    app.run(debug=True)