from .db import db
from sqlalchemy.sql import func

class CrimesVsPersons(db.Model):
    #Columns: Assault Offenses,Homicide Offenses,Human Trafficking,Kidnapping/ Abduction,Sex Offenses,state_id
    __tablename__ = 'crimes_vs_persons'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    assault_offenses = db.Column(db.Integer, nullable=False)
    homicide_offenses = db.Column(db.Integer, nullable=False)
    human_trafficking = db.Column(db.Integer, nullable=False)
    kidnapping_abduction = db.Column(db.Integer, nullable=False)
    sex_offenses = db.Column(db.Integer, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)

    # Relation
    state = db.relationship('State', back_populates='crimes_vs_persons')

    def to_dict(self):
        return {
            "id": self.id,
            "assault_offenses": self.assault_offenses,
            "homicide_offenses": self.homicide_offenses,
            "human_trafficking": self.human_trafficking,
            "kidnapping_abduction": self.kidnapping_abduction,
            "sex_offenses": self.sex_offenses,
            "state_id": self.state_id,
            "state": self.state.to_dict()
        }