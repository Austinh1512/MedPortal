from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)

@app.route("/")
def test():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)