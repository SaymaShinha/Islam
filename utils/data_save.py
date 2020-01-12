from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import requests, json


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://sayma:123@localhost:5432/islam"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Quran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(120), nullable=False)
    language = db.Column(db.String(80), unique=True, nullable=False)
    en_name = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable=False)
    format = db.Column(db.String(120), nullable=False)
    direction = db.Column(db.String(10))

@app.route('/data')
def save_data_in_database():
    response = requests.get("http://api.alquran.cloud/v1/edition")
    data = json.loads(response.content)["data"]
    quran = Quran(identifier='test', name='test', language=f'{datetime}', en_name='', type='', format='')
    db.session.add(quran)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)