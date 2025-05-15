"""
Script to generate a secure secret key for Flask application
"""
import secrets

# Generate a secure random 64-character hex key
secret_key = secrets.token_hex(32)

print(f"Generated new secret key: {secret_key}")
print("\nYou can add this to your .env file as:")
print(f"FLASK_SECRET_KEY={secret_key}")
