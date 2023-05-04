from .db import db
from sqlalchemy.sql import func

class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Columns: State,State Code
    state = db.Column(db.String(100), nullable=False)

    # Relation
    businesses = db.relationship('Business', back_populates='states')
    crimes_vs_persons = db.relationship('CrimesVsPerson', back_populates='states')  
    crimes_vs_property = db.relationship('CrimesVsProperty', back_populates='states')
    crimes_vs_society = db.relationship('CrimesVsSociety', back_populates='states')



    def to_dict(self):
        return {
            "id": self.id,
            "state": self.state,
            "businesses": [business.to_dict() for business in self.businesses]
        }