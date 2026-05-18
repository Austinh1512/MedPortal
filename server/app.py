from flask import Flask
from extensions import db
from dotenv import load_dotenv
import models
from routes import dashboard_bp, patients_bp, auth_bp
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db.init_app(app)

#Routes
app.register_blueprint(dashboard_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(auth_bp)
@app.route("/")
def test():
    return "Hello, World!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)