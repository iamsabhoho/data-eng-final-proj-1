from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    businesses = db.relationship('Business', back_populates='state', lazy=True)
    crimes_vs_person = db.relationship('CrimesVsPerson', backref='state', lazy=True)
    crimes_vs_property = db.relationship('CrimesVsProperty', backref='state', lazy=True)
    crimes_vs_society = db.relationship('CrimesVsSociety', backref='state', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }



class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.String(100))
    sales = db.Column(db.Float)
    city = db.Column(db.String(100))
    yoy_sales = db.Column(db.String(100))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    detail = db.Column(db.String(100))
    state = db.relationship('State', back_populates='businesses')

    def to_dict(self):
        return {
            'id': self.id,
            'restaurant': self.restaurant,
            'sales': self.sales,
            'city': self.city,
            'yoy_sales': self.yoy_sales,
            'state_id': self.state_id,
            'detail': self.detail,
            'state': self.state.to_dict()
        }
  
class CrimesVsPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assault_offenses = db.Column(db.Integer)
    homicide_offenses = db.Column(db.Integer)
    human_trafficking = db.Column(db.Integer)
    kidnapping_abduction = db.Column(db.Integer)
    sex_offenses = db.Column(db.Integer)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))

class CrimesVsProperty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_participating_agencies = db.Column(db.Integer)
    population_covered = db.Column(db.Integer)
    arson = db.Column(db.Integer)
    bribery = db.Column(db.Integer)
    burglary_breaking_entering = db.Column(db.Integer)
    counterfeiting_forgery = db.Column(db.Integer)
    destruction_damage_vandalism = db.Column(db.Integer)
    embezzlement = db.Column(db.Integer)
    extortion_blackmail = db.Column(db.Integer)
    fraud_offenses = db.Column(db.Integer)
    larceny_theft_offenses = db.Column(db.Integer)
    motor_vehicle_theft = db.Column(db.Integer)
    robbery = db.Column(db.Integer)
    stolen_property_offenses = db.Column(db.Integer)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))

class CrimesVsSociety(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_cruelty = db.Column(db.Integer)
    drug_narcotic_offenses = db.Column(db.Integer)
    gambling_offenses = db.Column(db.Integer)
    pornography_obscene_material = db.Column(db.Integer)
    prostitution_offenses = db.Column(db.Integer)
    weapon_law_violations = db.Column(db.Integer)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))


db.create_all()


def populate_db():
    # with app.app_context():
    # Read CSV files
    business_df = pd.read_csv('business_df.csv')
    state_df = pd.read_csv('state_df.csv')
    crimes_vs_person_df = pd.read_csv('crime_person.csv')
    crimes_vs_property_df = pd.read_csv('crime_property.csv')
    crimes_vs_society_df = pd.read_csv('crime_society.csv')

    # Add States
    for _, row in state_df.iterrows():
        # Check if the state already exists in the database
        state = State.query.filter_by(name=row['State']).first()
        if state is None:
            state = State(name=row['State'])
            db.session.add(state)


    # Add Businesses
    for _, row in business_df.iterrows():
        business = Business(restaurant=row['Restaurant'],
                            sales=row['Sales'],
                            city=row['City'],
                            yoy_sales=row['YOY_Sales'],
                            state_id=row['state_id'],
                            detail=row['details']
                            )
        db.session.add(business)

    # Add CrimesVsPerson
    for _, row in crimes_vs_person_df.iterrows():
        crime = CrimesVsPerson(assault_offenses=row['Assault Offenses'],
                                homicide_offenses=row['Homicide Offenses'],
                                human_trafficking=row['Human Trafficking'],
                                kidnapping_abduction=row['Kidnapping/ Abduction'],
                                sex_offenses=row['Sex Offenses'],
                                state_id=row['state_id'])
        db.session.add(crime)

    # Add CrimesVsProperty
    for _, row in crimes_vs_property_df.iterrows():
        crime = CrimesVsProperty(number_of_participating_agencies=row['Number of Participating Agencies'],
                                population_covered=row['Population Covered'],
                                arson=row['Arson'],
                                bribery=row['Bribery'],
                                burglary_breaking_entering=row['Burglary/Breaking & Entering'],
                                counterfeiting_forgery=row['Counterfeiting/Forgery'],
                                destruction_damage_vandalism=row['Destruction/Damage/Vandalism'],
                                embezzlement=row['Embezzlement'],
                                extortion_blackmail=row['Extortion/Blackmail'],
                                fraud_offenses=row['Fraud Offenses'],
                                larceny_theft_offenses=row['Larceny/Theft Offenses'],
                                motor_vehicle_theft=row['Motor Vehicle Theft'],
                                robbery=row['Robbery'],
                                stolen_property_offenses=row['Stolen Property Offenses'],
                                state_id=row['state_id'],)
        db.session.add(crime)

    # Add CrimesVsSociety
    for _, row in crimes_vs_society_df.iterrows():
        crime = CrimesVsSociety(animal_cruelty=row['Animal Cruelty'],
                                drug_narcotic_offenses=row['Drug/Narcotic Offenses'],
                                gambling_offenses=row['Gambling Offenses'],
                                pornography_obscene_material=row['Pornography/Obscene Material'],
                                prostitution_offenses=row['Prostitution Offenses'],
                                weapon_law_violations=row['Weapon Law Violations'],
                                state_id=row['state_id'])
        db.session.add(crime)

    db.session.commit()

# Uncomment the following line to populate the database
populate_db()

@app.route('/api/businesses/<state_name>')
def get_businesses_by_state(state_name):
    businesses = Business.query.join(State).filter(State.name == state_name).all()
    result = []

    for business in businesses:
        result.append({
            'id': business.id,
            'restaurant': business.restaurant,
            'sales': business.sales,
            'city': business.city,
            'state': business.state.name,
            'yoy_sales': business.yoy_sales,
            'state_id': business.state_id
        })

    if len(result) == 0:
        return jsonify({'error': 'Data not found'}), 404

    return jsonify(result)


@app.route('/api/business/<int:business_id>/crimes')
def get_business_crimes_info(business_id):
    business = Business.query.get_or_404(business_id)

    crimes_vs_person = CrimesVsPerson.query.filter_by(state_id=business.state_id).first()
    crimes_vs_property = CrimesVsProperty.query.filter_by(state_id=business.state_id).first()
    crimes_vs_society = CrimesVsSociety.query.filter_by(state_id=business.state_id).first()

    business_info = {
        'id': business.id,
        'restaurant': business.restaurant,
        'sales': business.sales,
        'city': business.city,
        'state': business.state.name,
        'yoy_sales': business.yoy_sales,
        'state_id': business.state_id
    }

    if not crimes_vs_person:
        return jsonify({'error': 'Data not found'}), 404

    crimes_info = {
        'crimes_vs_person': {
            'assault_offenses': crimes_vs_person.assault_offenses,
            'homicide_offenses': crimes_vs_person.homicide_offenses,
            'human_trafficking': crimes_vs_person.human_trafficking,
            'kidnapping_abduction': crimes_vs_person.kidnapping_abduction,
            'sex_offenses': crimes_vs_person.sex_offenses,
        },
        'crimes_vs_property': {
            'number_of_participating_agencies': crimes_vs_property.number_of_participating_agencies,
            'population_covered': crimes_vs_property.population_covered,
            'arson': crimes_vs_property.arson,
            'bribery': crimes_vs_property.bribery,
            'burglary_breaking_entering': crimes_vs_property.burglary_breaking_entering,
            'counterfeiting_forgery': crimes_vs_property.counterfeiting_forgery,
            'destruction_damage_vandalism': crimes_vs_property.destruction_damage_vandalism,
            'embezzlement': crimes_vs_property.embezzlement,
            'extortion_blackmail': crimes_vs_property.extortion_blackmail,
            'fraud_offenses': crimes_vs_property.fraud_offenses,
            'larceny_theft_offenses': crimes_vs_property.larceny_theft_offenses,
            'motor_vehicle_theft': crimes_vs_property.motor_vehicle_theft,
            'robbery': crimes_vs_property.robbery,
            'stolen_property_offenses': crimes_vs_property.stolen_property_offenses,
        },
        'crimes_vs_society': {
            'animal_cruelty': crimes_vs_society.animal_cruelty,
            'drug_narcotic_offenses': crimes_vs_society.drug_narcotic_offenses,
            'gambling_offenses': crimes_vs_society.gambling_offenses,
            'pornography_obscene_material': crimes_vs_society.pornography_obscene_material,
            'prostitution_offenses': crimes_vs_society.prostitution_offenses,
            'weapon_law_violations': crimes_vs_society.weapon_law_violations,
        }
    }

    response = {
        'business': business_info,
        'crimes': crimes_info
    }

    return jsonify(response)


if __name__ == '__main__':
    with app.app_context():
        # Uncomment the following line to populate the database
        # populate_db()
        app.run(debug=True)

