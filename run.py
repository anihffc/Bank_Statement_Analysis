from backend.app import app as backend_app
from threading import Thread

# Run the Flask app
if __name__ == "__main__":
    backend_app.run(debug=True)
