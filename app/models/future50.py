from .db import db
from sqlalchemy.sql import func

class Future50(db.Model):   
    __tablename__ = 'future50'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Colunms: Rank	Restaurant	Sales	YOY_Sales	Units	YOY_Units	Unit_Volume	Franchising	City	State
    rank = db.Column(db.Integer, nullable=False)
    restaurant = db.Column(db.String(100), nullable=False)
    sales = db.Column(db.Float, nullable=False)
    yoy_sales = db.Column(db.Float, nullable=False)
    units = db.Column(db.Integer, nullable=False)
    yoy_units = db.Column(db.Float, nullable=False)
    unit_volume = db.Column(db.Float, nullable=False)
    franchising = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)

    # Relation TBD
    
