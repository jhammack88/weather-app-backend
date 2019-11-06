from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
from flask_heroku import Heroku
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://fpnuyvfspzyjyl:c271ca19c0f8cf2a5ebb00994489c801c25f2d6b5a21de88b5fc1844cbe4618c@ec2-23-21-94-99.compute-1.amazonaws.com:5432/d84ot1u7lrqjvl"
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(144), unique=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

#Endpoint to create a new review
@app.route('/review', methods=["POST"])
def add_review():
    title = request.json['title']
    content = request.json['content']

    new_review = Review(title, content)

    db.session.add(new_review)
    db.session.commit()

    review = Review.query.get(new_review.id)

    return review_schema.jsonify(review)

# Endpoint to query all reviews
@app.route("/reviews", methods=["GET"])
def get_reviews():
    all_reviews = Review.query.all()
    result = reviews_schema.dump(all_reviews)
    return jsonify(result)

# Endpoint for querying a single review
@app.route("/review/<id>", methods=["GET"])
def get_review(id):
    review = Review.query.get(id)
    return review_schema.jsonify(review)

# Endpoint for updating a review
@app.route("/review/<id>", methods=["PUT"])
def review_update(id):
    review = Review.query.get(id)
    title = request.json['title']
    content = request.json['content']
    
    review.title = title
    review.content = content

    db.session.commit()
    return review_schema.jsonify(review)

# Endpoint for deleting a record
@app.route("/review/<id>", methods=["DELETE"])
def review_delete(id):
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()

    return "Review was successfully deleted"

if __name__ == '__main__':
    app.run(debug=True)