import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.models import db

# Create the Flask application using create_app()
app = create_app()

# Configure database
from config import Config


app.config.from_object(Config)

# Initialize database


db.init_app(app)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("=" * 60)
    print("API RGPD - Server started with Flask-RESTX")
    print("URL: http://localhost:5000")
    print("Swagger Documentation: http://localhost:5000/docs")
    print("CORS enabled for: localhost:3000")
    print("\nAvailable routes:")
    print("  - POST /api/users/register")
    print("  - POST /api/users/login")
    print("  - GET  /api/users/")
    print("  - GET  /api/users/<user_id>")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
