from .db import db
from sqlalchemy.sql import func

class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Columns: Restaurant,Sales,City,State,YOY_Sales,state_id
    restaurant = db.Column(db.String(100), nullable=False)
    sales = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    yoy_sales = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    business_detail = db.Column(db.String(100), nullable=False)

    # Relation
    states = db.relationship('State', back_populates='businesses')

    def to_dict(self):
        return {
            "id": self.id,
            "restaurant": self.restaurant,
            "sales": self.sales,
            "city": self.city,
            "yoy_sales": self.yoy_sales,
            "state_id": self.state_id,
            "state": self.state.to_dict()
        }


