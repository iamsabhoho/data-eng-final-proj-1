from .db import db
from sqlalchemy.sql import func

class CrimesVsProperty(db.Model):
    # Columns: State,Number of Participating Agencies,Population Covered,Arson,Bribery,Burglary/Breaking & Entering,Counterfeiting/Forgery,Destruction/Damage/Vandalism,Embezzlement,Extortion/Blackmail,Fraud Offenses,Larceny/Theft Offenses,Motor Vehicle Theft,Robbery,Stolen Property Offenses,state_id
    __tablename__ = 'crimes_vs_properties'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    number_of_participating_agencies = db.Column(db.Integer, nullable=False)
    population_covered = db.Column(db.Integer, nullable=False)
    arson = db.Column(db.Integer, nullable=False)
    bribery = db.Column(db.Integer, nullable=False)
    burglary_breaking_entering = db.Column(db.Integer, nullable=False)
    counterfeiting_forgery = db.Column(db.Integer, nullable=False)
    destruction_damage_vandalism = db.Column(db.Integer, nullable=False)
    embezzlement = db.Column(db.Integer, nullable=False)
    extortion_blackmail = db.Column(db.Integer, nullable=False)
    fraud_offenses = db.Column(db.Integer, nullable=False)
    larceny_theft_offenses = db.Column(db.Integer, nullable=False)
    motor_vehicle_theft = db.Column(db.Integer, nullable=False)
    robbery = db.Column(db.Integer, nullable=False)
    stolen_property_offenses = db.Column(db.Integer, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)

    # Relation
    states = db.relationship('State', back_populates='crimes_vs_property')

    def to_dict(self):
        return {
            "id": self.id,
            "number_of_participating_agencies": self.number_of_participating_agencies,
            "population_covered": self.population_covered,
            "arson": self.arson,
            "bribery": self.bribery,
            "burglary_breaking_entering": self.burglary_breaking_entering,
            "counterfeiting_forgery": self.counterfeiting_forgery,
            "destruction_damage_vandalism": self.destruction_damage_vandalism,
            "embezzlement": self.embezzlement,
            "extortion_blackmail": self.extortion_blackmail,
            "fraud_offenses": self.fraud_offenses,
            "larceny_theft_offenses": self.larceny_theft_offenses,
            "motor_vehicle_theft": self.motor_vehicle_theft,
            "robbery": self.robbery,
            "stolen_property_offenses": self.stolen_property_offenses,
            "state_id": self.state_id,
            "state": self.state.to_dict()
        }