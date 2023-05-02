from .db import db
from sqlalchemy.sql import func

class BusinessDetail(db.Model):
    __tablename__ = 'business_details'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Columns: chain,independent,future
    chain = db.Column(db.Boolean, nullable=False)
    independent = db.Column(db.Boolean, nullable=False)
    future = db.Column(db.Boolean, nullable=False)

    # Relation
    business = db.relationship('Business', back_populates='business_detail')

    def to_dict(self):
        return {
            "id": self.id,
            "chain": self.chain,
            "independent": self.independent,
            "future": self.future,
            "business": self.business.to_dict()
        }