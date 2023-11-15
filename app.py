from flask import Flask, jsonify, render_template, request
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func


app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

Bootstrap4(app)


# Cafe Config
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


# Home Page
@app.route("/")
def home():
    db_cafes = db.session.execute(db.select(Cafe).order_by('id')).scalars()
    cafes = [cafe for cafe in db_cafes]
    return render_template("index.html", cafes=cafes)


@app.route("/cafe/<int:cafe_id>")
def cafe(cafe_id):
    cafe_page = db.get_or_404(Cafe, cafe_id)
    return render_template("cafe.html", cafe=cafe_page)


if __name__ == '__main__':
    app.run(debug=True)
