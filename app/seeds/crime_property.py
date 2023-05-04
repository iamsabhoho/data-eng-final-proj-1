from app.models import db, Business, CrimesVsPerson, CrimesVsProperty, CrimesVsSociety, State
import pandas as pd
import os

csv_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '', 'crime_property.csv')

crime_property = pd.read_csv(csv_file_path)

crime_property_list = []


for index, row in crime_property.iterrows():
     # Columns: State,Number of Participating Agencies,Population Covered,Arson,Bribery,Burglary/Breaking & Entering,Counterfeiting/Forgery,Destruction/Damage/Vandalism,Embezzlement,Extortion/Blackmail,Fraud Offenses,Larceny/Theft Offenses,Motor Vehicle Theft,Robbery,Stolen Property Offenses,state_id
    crime_property_list.append(CrimesVsProperty(
        number_of_participating_agencies=row['Number of Participating Agencies'],
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
        state_id=row['state_id']
        ))
    
def seed_crime_property():
    for crime_property in crime_property_list:
        db.session.add(crime_property)
        db.session.commit()

def undo_crime_property():
    for crime_property in crime_property_list:
        db.session.delete(crime_property)
        db.session.commit()


    