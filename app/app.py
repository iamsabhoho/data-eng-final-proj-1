from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import plotly.express as px
import plotly 
import json


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

@app.route('/api/business/add_data', methods=['POST'])
def add_business():
    data = request.get_json()
    #Add new business
    new_business = Business(restaurant=data['business']['restaurant'],
                            sales=data['business']['sales'],
                            city=data['business']['city'],
                            yoy_sales=data['business']['yoy_sales'],
                            state_id=data['business']['state_id'],
                            detail=data['business']['detail'])
    #Add crime to databases
    new_crimes_vs_person = CrimesVsPerson(
        assault_offenses=data['crimes']['crimes_vs_person']['assault_offenses'],
        homicide_offenses=data['crimes']['crimes_vs_person']['homicide_offenses'],
        human_trafficking=data['crimes']['crimes_vs_person']['human_trafficking'],
        kidnapping_abduction=data['crimes']['crimes_vs_person']['kidnapping_abduction'],
        sex_offenses=data['crimes']['crimes_vs_person']['sex_offenses'],
        state=new_business.state
    )

    new_crimes_vs_property = CrimesVsProperty(
        number_of_participating_agencies=data['crimes']['crimes_vs_property']['number_of_participating_agencies'],
        population_covered=data['crimes']['crimes_vs_property']['population_covered'],
        arson=data['crimes']['crimes_vs_property']['arson'],
        bribery=data['crimes']['crimes_vs_property']['bribery'],
        burglary_breaking_entering=data['crimes']['crimes_vs_property']['burglary_breaking_entering'],
        counterfeiting_forgery=data['crimes']['crimes_vs_property']['counterfeiting_forgery'],
        destruction_damage_vandalism=data['crimes']['crimes_vs_property']['destruction_damage_vandalism'],
        embezzlement=data['crimes']['crimes_vs_property']['embezzlement'],
        extortion_blackmail=data['crimes']['crimes_vs_property']['extortion_blackmail'],
        fraud_offenses=data['crimes']['crimes_vs_property']['fraud_offenses'],
        larceny_theft_offenses=data['crimes']['crimes_vs_property']['larceny_theft_offenses'],
        motor_vehicle_theft=data['crimes']['crimes_vs_property']['motor_vehicle_theft'],
        robbery=data['crimes']['crimes_vs_property']['robbery'],
        stolen_property_offenses=data['crimes']['crimes_vs_property']['stolen_property_offenses'],
        state=new_business.state
    )

    new_crimes_vs_society = CrimesVsSociety(
        animal_cruelty=data['crimes']['crimes_vs_society']['animal_cruelty'],
        drug_narcotic_offenses=data['crimes']['crimes_vs_society']['drug_narcotic_offenses'],
        gambling_offenses=data['crimes']['crimes_vs_society']['gambling_offenses'],
        pornography_obscene_material=data['crimes']['crimes_vs_society']['pornography_obscene_material'],
        prostitution_offenses=data['crimes']['crimes_vs_society']['prostitution_offenses'],
        weapon_law_violations=data['crimes']['crimes_vs_society']['weapon_law_violations'],
        state=new_business.state
    )

    # Add new instances to the database session and commit changes
    db.session.add_all([new_business, new_crimes_vs_person, new_crimes_vs_property, new_crimes_vs_society])
    db.session.commit()

    response = {
        'business': {
            'restaurant': new_business.restaurant,
            'sales': new_business.sales,
            'city': new_business.city,
            'yoy_sales': new_business.yoy_sales,
            'state_id': new_business.state_id,
            'detail': new_business.detail,
        },
        'crimes_vs_person': {
            'assault_offenses': new_crimes_vs_person.assault_offenses,
            'homicide_offenses': new_crimes_vs_person.homicide_offenses,
            'human_trafficking': new_crimes_vs_person.human_trafficking,
            'kidnapping_abduction': new_crimes_vs_person.kidnapping_abduction,
            'sex_offenses': new_crimes_vs_person.sex_offenses,
        },
        'crimes_vs_property': {
            'number_of_participating_agencies': new_crimes_vs_property.number_of_participating_agencies,
            'population_covered': new_crimes_vs_property.population_covered,
            'arson': new_crimes_vs_property.arson,
            'bribery': new_crimes_vs_property.bribery,
            'burglary_breaking_entering': new_crimes_vs_property.burglary_breaking_entering,
            'counterfeiting_forgery': new_crimes_vs_property.counterfeiting_forgery,
            'destruction_damage_vandalism': new_crimes_vs_property.destruction_damage_vandalism,
            'embezzlement': new_crimes_vs_property.embezzlement,
            'extortion_blackmail': new_crimes_vs_property.extortion_blackmail,
            'fraud_offenses': new_crimes_vs_property.fraud_offenses,
            'larceny_theft_offenses': new_crimes_vs_property.larceny_theft_offenses,
            'motor_vehicle_theft': new_crimes_vs_property.motor_vehicle_theft,
            'robbery': new_crimes_vs_property.robbery,
            'stolen_property_offenses': new_crimes_vs_property.stolen_property_offenses,
        },
        'crimes_vs_society': {
            'animal_cruelty': new_crimes_vs_society.animal_cruelty,
            'drug_narcotic_offenses': new_crimes_vs_society.drug_narcotic_offenses,
            'gambling_offenses': new_crimes_vs_society.gambling_offenses,
            'pornography_obscene_material': new_crimes_vs_society.pornography_obscene_material,
            'prostitution_offenses': new_crimes_vs_society.prostitution_offenses,
            'weapon_law_violations': new_crimes_vs_society.weapon_law_violations,
        }
    }

    return jsonify(response)


@app.route('/api/generate_report', methods=['GET'])
def report():
    """
    Generates plotly report of the data. 
    """

    business = Business
    state = State.query.all()
    state_res = []
    for s in state:
        state_res.append({
            'id': s.id,
            'state':s.name,
        })
    state_res = pd.DataFrame(state_res)
    
    cvprop = CrimesVsProperty
    cvs = CrimesVsSociety

    businesses = Business.query.join(State).all()
    business_result = []

    for business in businesses:
        business_result.append({
            'id': business.id,
            'restaurant': business.restaurant,
            'sales': business.sales,
            'city': business.city,
            'state': business.state.name,
            'yoy_sales': business.yoy_sales
        })
    business_result = pd.DataFrame(business_result)


    business_agg = business_result.groupby('state').agg('sum').reset_index()
    
    business_agg = business_agg.merge(state_res, on = 'state', how = 'right', suffixes=('_x', '_state'))
    business_agg['state_id'] = business_agg['id_state']
    business_agg = business_agg.drop('id_state', axis = 1)
    
    cvpers = CrimesVsPerson.query.join(State).all()
    cvpers_results = []

    for crimeperson in cvpers:
        cvpers_results.append({
            'assault_offenses': crimeperson.assault_offenses,
            'homicide_offenses': crimeperson.homicide_offenses,
            'human_trafficking': crimeperson.human_trafficking,
            'kidnapping_abduction': crimeperson.kidnapping_abduction,
            'sex_offenses': crimeperson.sex_offenses,
            'state_id': crimeperson.state_id,
        })

    cvpers_results = pd.DataFrame(cvpers_results).groupby('state_id').agg('sum').reset_index()
    
    agg_res = cvpers_results.merge(business_agg, on = 'state_id', how = 'inner')


    us_state_to_abbrev = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC",
        "American Samoa": "AS",
        "Guam": "GU",
        "Northern Mariana Islands": "MP",
        "Puerto Rico": "PR",
        "United States Minor Outlying Islands": "UM",
        "U.S. Virgin Islands": "VI",
        }

    agg_res['state'] = agg_res['state'].apply(lambda x: us_state_to_abbrev[x])

    
    fig1 = px.bar(business_agg, x = 'state', y = 'sales', title = 'Total sales of each state')
    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    map_figure = px.choropleth(agg_res, 
                               locations = 'state', 
                               color = 'homicide_offenses', 
                               color_continuous_scale="Viridis_r",
                               locationmode="USA-states",
                               scope = 'usa',
                               title = 'Total Homicides in each State')
    
    print(agg_res.columns)
    scatter = px.scatter(agg_res, x = 'sales', y = 'homicide_offenses',
                         title = 'Sales v.s. Homicides',
                         trendline = 'ols')
    
    stateSales = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    mapfigure = json.dumps(map_figure, cls=plotly.utils.PlotlyJSONEncoder)
    scatter = json.dumps(scatter, cls=plotly.utils.PlotlyJSONEncoder)



    return render_template('notdash.html', stateSales=stateSales, 
                           mapfigure = mapfigure,
                           scatter = scatter)

@app.route('/api/business/delete_data', methods=['DELETE'])
def delete_data():
    data = request.get_json()

    # delete business
    delete_business = Business(restaurant=data['business']['restaurant'],
                            sales=data['business']['sales'],
                            city=data['business']['city'],
                            yoy_sales=data['business']['yoy_sales'],
                            state_id=data['business']['state_id'],
                            detail=data['business']['detail'])

    # delete crime vs person
    delete_crimes_vs_person = CrimesVsPerson(
        assault_offenses=data['crimes']['crimes_vs_person']['assault_offenses'],
        homicide_offenses=data['crimes']['crimes_vs_person']['homicide_offenses'],
        human_trafficking=data['crimes']['crimes_vs_person']['human_trafficking'],
        kidnapping_abduction=data['crimes']['crimes_vs_person']['kidnapping_abduction'],
        sex_offenses=data['crimes']['crimes_vs_person']['sex_offenses'],
        state=delete_business.state
    )

    # delete crime vs property
    delete_crimes_vs_property = CrimesVsProperty(
        number_of_participating_agencies=data['crimes']['crimes_vs_property']['number_of_participating_agencies'],
        population_covered=data['crimes']['crimes_vs_property']['population_covered'],
        arson=data['crimes']['crimes_vs_property']['arson'],
        bribery=data['crimes']['crimes_vs_property']['bribery'],
        burglary_breaking_entering=data['crimes']['crimes_vs_property']['burglary_breaking_entering'],
        counterfeiting_forgery=data['crimes']['crimes_vs_property']['counterfeiting_forgery'],
        destruction_damage_vandalism=data['crimes']['crimes_vs_property']['destruction_damage_vandalism'],
        embezzlement=data['crimes']['crimes_vs_property']['embezzlement'],
        extortion_blackmail=data['crimes']['crimes_vs_property']['extortion_blackmail'],
        fraud_offenses=data['crimes']['crimes_vs_property']['fraud_offenses'],
        larceny_theft_offenses=data['crimes']['crimes_vs_property']['larceny_theft_offenses'],
        motor_vehicle_theft=data['crimes']['crimes_vs_property']['motor_vehicle_theft'],
        robbery=data['crimes']['crimes_vs_property']['robbery'],
        stolen_property_offenses=data['crimes']['crimes_vs_property']['stolen_property_offenses'],
        state=delete_business.state
    )

    # delete crime vs society
    delete_crimes_vs_society = CrimesVsSociety(
        animal_cruelty=data['crimes']['crimes_vs_society']['animal_cruelty'],
        drug_narcotic_offenses=data['crimes']['crimes_vs_society']['drug_narcotic_offenses'],
        gambling_offenses=data['crimes']['crimes_vs_society']['gambling_offenses'],
        pornography_obscene_material=data['crimes']['crimes_vs_society']['pornography_obscene_material'],
        prostitution_offenses=data['crimes']['crimes_vs_society']['prostitution_offenses'],
        weapon_law_violations=data['crimes']['crimes_vs_society']['weapon_law_violations'],
        state=delete_business.state
    )

    # delete the tables and commit changes
    db.session.delete(delete_business)
    db.session.delete(delete_crimes_vs_person)
    db.session.delete(delete_crimes_vs_property)
    db.session.delete(delete_crimes_vs_society)
    db.session.commit()

    response = {
        'business': {
            'restaurant': delete_business.restaurant,
            'sales': delete_business.sales,
            'city': delete_business.city,
            'yoy_sales': delete_business.yoy_sales,
            'state_id': delete_business.state_id,
            'detail': delete_business.detail,
        },
        'crimes_vs_person': {
            'assault_offenses': delete_crimes_vs_person.assault_offenses,
            'homicide_offenses': delete_crimes_vs_person.homicide_offenses,
            'human_trafficking': delete_crimes_vs_person.human_trafficking,
            'kidnapping_abduction': delete_crimes_vs_person.kidnapping_abduction,
            'sex_offenses': delete_crimes_vs_person.sex_offenses,
        },
        'crimes_vs_property': {
            'number_of_participating_agencies': delete_crimes_vs_property.number_of_participating_agencies,
            'population_covered': delete_crimes_vs_property.population_covered,
            'arson': delete_crimes_vs_property.arson,
            'bribery': delete_crimes_vs_property.bribery,
            'burglary_breaking_entering': delete_crimes_vs_property.burglary_breaking_entering,
            'counterfeiting_forgery': delete_crimes_vs_property.counterfeiting_forgery,
            'destruction_damage_vandalism': delete_crimes_vs_property.destruction_damage_vandalism,
            'embezzlement': delete_crimes_vs_property.embezzlement,
            'extortion_blackmail': delete_crimes_vs_property.extortion_blackmail,
            'fraud_offenses': delete_crimes_vs_property.fraud_offenses,
            'larceny_theft_offenses': delete_crimes_vs_property.larceny_theft_offenses,
            'motor_vehicle_theft': delete_crimes_vs_property.motor_vehicle_theft,
            'robbery': delete_crimes_vs_property.robbery,
            'stolen_property_offenses': delete_crimes_vs_property.stolen_property_offenses,
        },
        'crimes_vs_society': {
            'animal_cruelty': delete_crimes_vs_society.animal_cruelty,
            'drug_narcotic_offenses': delete_crimes_vs_society.drug_narcotic_offenses,
            'gambling_offenses': delete_crimes_vs_society.gambling_offenses,
            'pornography_obscene_material': delete_crimes_vs_society.pornography_obscene_material,
            'prostitution_offenses': delete_crimes_vs_society.prostitution_offenses,
            'weapon_law_violations': delete_crimes_vs_society.weapon_law_violations,
        }
    }

    return jsonify(response)

@app.route('/api/business/update_data', methods=['PUT'])
def update_data():
    data = request.get_json()

    # update business
    update_business = Business(restaurant=data['business']['restaurant'],
                            sales=data['business']['sales'],
                            city=data['business']['city'],
                            yoy_sales=data['business']['yoy_sales'],
                            state_id=data['business']['state_id'],
                            detail=data['business']['detail'])

    # update crime vs person
    update_crimes_vs_person = CrimesVsPerson(
        assault_offenses=data['crimes']['crimes_vs_person']['assault_offenses'],
        homicide_offenses=data['crimes']['crimes_vs_person']['homicide_offenses'],
        human_trafficking=data['crimes']['crimes_vs_person']['human_trafficking'],
        kidnapping_abduction=data['crimes']['crimes_vs_person']['kidnapping_abduction'],
        sex_offenses=data['crimes']['crimes_vs_person']['sex_offenses'],
        state=update_business.state
    )

    # update crime vs property
    update_crimes_vs_property = CrimesVsProperty(
        number_of_participating_agencies=data['crimes']['crimes_vs_property']['number_of_participating_agencies'],
        population_covered=data['crimes']['crimes_vs_property']['population_covered'],
        arson=data['crimes']['crimes_vs_property']['arson'],
        bribery=data['crimes']['crimes_vs_property']['bribery'],
        burglary_breaking_entering=data['crimes']['crimes_vs_property']['burglary_breaking_entering'],
        counterfeiting_forgery=data['crimes']['crimes_vs_property']['counterfeiting_forgery'],
        destruction_damage_vandalism=data['crimes']['crimes_vs_property']['destruction_damage_vandalism'],
        embezzlement=data['crimes']['crimes_vs_property']['embezzlement'],
        extortion_blackmail=data['crimes']['crimes_vs_property']['extortion_blackmail'],
        fraud_offenses=data['crimes']['crimes_vs_property']['fraud_offenses'],
        larceny_theft_offenses=data['crimes']['crimes_vs_property']['larceny_theft_offenses'],
        motor_vehicle_theft=data['crimes']['crimes_vs_property']['motor_vehicle_theft'],
        robbery=data['crimes']['crimes_vs_property']['robbery'],
        stolen_property_offenses=data['crimes']['crimes_vs_property']['stolen_property_offenses'],
        state=update_business.state
    )

    # update crime vs society
    update_crimes_vs_society = CrimesVsSociety(
        animal_cruelty=data['crimes']['crimes_vs_society']['animal_cruelty'],
        drug_narcotic_offenses=data['crimes']['crimes_vs_society']['drug_narcotic_offenses'],
        gambling_offenses=data['crimes']['crimes_vs_society']['gambling_offenses'],
        pornography_obscene_material=data['crimes']['crimes_vs_society']['pornography_obscene_material'],
        prostitution_offenses=data['crimes']['crimes_vs_society']['prostitution_offenses'],
        weapon_law_violations=data['crimes']['crimes_vs_society']['weapon_law_violations'],
        state=update_business.state
    )

    # update the tables and commit changes
    db.session.update(update_business)
    db.session.update(update_crimes_vs_person)
    db.session.update(update_crimes_vs_property)
    db.session.update(update_crimes_vs_society)
    db.session.commit()

    response = {
        'business': {
            'restaurant': update_business.restaurant,
            'sales': update_business.sales,
            'city': update_business.city,
            'yoy_sales': update_business.yoy_sales,
            'state_id': update_business.state_id,
            'detail': update_business.detail,
        },
        'crimes_vs_person': {
            'assault_offenses': update_crimes_vs_person.assault_offenses,
            'homicide_offenses': update_crimes_vs_person.homicide_offenses,
            'human_trafficking': update_crimes_vs_person.human_trafficking,
            'kidnapping_abduction': update_crimes_vs_person.kidnapping_abduction,
            'sex_offenses': update_crimes_vs_person.sex_offenses,
        },
        'crimes_vs_property': {
            'number_of_participating_agencies': update_crimes_vs_property.number_of_participating_agencies,
            'population_covered': update_crimes_vs_property.population_covered,
            'arson': update_crimes_vs_property.arson,
            'bribery': update_crimes_vs_property.bribery,
            'burglary_breaking_entering': update_crimes_vs_property.burglary_breaking_entering,
            'counterfeiting_forgery': update_crimes_vs_property.counterfeiting_forgery,
            'destruction_damage_vandalism': update_crimes_vs_property.destruction_damage_vandalism,
            'embezzlement': update_crimes_vs_property.embezzlement,
            'extortion_blackmail': update_crimes_vs_property.extortion_blackmail,
            'fraud_offenses': update_crimes_vs_property.fraud_offenses,
            'larceny_theft_offenses': update_crimes_vs_property.larceny_theft_offenses,
            'motor_vehicle_theft': update_crimes_vs_property.motor_vehicle_theft,
            'robbery': update_crimes_vs_property.robbery,
            'stolen_property_offenses': update_crimes_vs_property.stolen_property_offenses,
        },
        'crimes_vs_society': {
            'animal_cruelty': update_crimes_vs_society.animal_cruelty,
            'drug_narcotic_offenses': update_crimes_vs_society.drug_narcotic_offenses,
            'gambling_offenses': update_crimes_vs_society.gambling_offenses,
            'pornography_obscene_material': update_crimes_vs_society.pornography_obscene_material,
            'prostitution_offenses': update_crimes_vs_society.prostitution_offenses,
            'weapon_law_violations': update_crimes_vs_society.weapon_law_violations,
        }
    }

    return jsonify(response)

    

if __name__ == '__main__':
    with app.app_context():
        # Uncomment the following line to populate the database
        # populate_db()
        app.run(debug=True)

