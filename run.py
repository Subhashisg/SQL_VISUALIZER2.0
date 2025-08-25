from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run in debug mode for development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"Starting SQL Visualizer on http://localhost:{port}")
    print("Make sure to:")
    print("1. Set up your .env file with SECRET_KEY and ENCRYPTION_KEY")
    print("2. Get your Gemini API key from https://makersuite.google.com/app/apikey")
    print("3. Add your API key in the application settings after registration")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
