from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from extensions import db
from dotenv import load_dotenv
import models
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db.init_app(app)

@app.route("/")
def test():
    return "Hello, World!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)