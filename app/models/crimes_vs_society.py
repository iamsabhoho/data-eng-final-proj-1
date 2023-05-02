from .db import db
from sqlalchemy.sql import func

class CrimesVsSociety(db.Model):

    __tablename__ = 'crimes_vs_society'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Columns: State,Animal Cruelty,Drug/Narcotic Offenses,Gambling Offenses,Pornography/Obscene Material,Prostitution Offenses,Weapon Law Violations,state_id
    animal_cruelty = db.Column(db.Integer, nullable=False)
    drug_narcotic_offenses = db.Column(db.Integer, nullable=False)
    gambling_offenses = db.Column(db.Integer, nullable=False)
    pornography_obscene_material = db.Column(db.Integer, nullable=False)
    prostitution_offenses = db.Column(db.Integer, nullable=False)
    weapon_law_violations = db.Column(db.Integer, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)

    # Relation
    state = db.relationship('State', back_populates='crimes_vs_society')

    def to_dict(self):
        return {
            "id": self.id,
            "animal_cruelty": self.animal_cruelty,
            "drug_narcotic_offenses": self.drug_narcotic_offenses,
            "gambling_offenses": self.gambling_offenses,
            "pornography_obscene_material": self.pornography_obscene_material,
            "prostitution_offenses": self.prostitution_offenses,
            "weapon_law_violations": self.weapon_law_violations,
            "state_id": self.state_id,
            "state": self.state.to_dict()
        }

        



  




