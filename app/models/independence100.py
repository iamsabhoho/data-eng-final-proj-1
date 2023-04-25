from .db import db
from sqlalchemy.sql import func

class Independence100(db.Model):
    __tablename__ = 'independence100'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # columns: Rank	Restaurant	Sales	Average Check	City	State	Meals_Served
    rank = db.Column(db.Integer, nullable=False)
    restaurant = db.Column(db.String(100), nullable=False)
    sales = db.Column(db.Float, nullable=False)
    average_check = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    meals_served = db.Column(db.Integer, nullable=False)

    # Relation TBD

