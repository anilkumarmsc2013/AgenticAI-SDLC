from flask import Flask
from api import app as api_app
from config import DATABASE_URL

app = Flask(__name__)

# Initialize database connection 

# ...

if __name__ == '__main__':
    app.run(debug=True)