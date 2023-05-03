from app.models import db, Business, BusinessDetail, CrimesVsPerson, CrimesVsProperty, CrimesVsSociety, State
import pandas as pd

crime_society = pd.read_csv('crime_society.csv')

crime_society_list = []

for index, row in crime_society.iterrows():
    # Columns: State,Animal Cruelty,Drug/Narcotic Offenses,Gambling Offenses,Pornography/Obscene Material,Prostitution Offenses,Weapon Law Violations,state_id
    crime_society_list.append(CrimesVsSociety(
        animal_cruelty=row['Animal Cruelty'],
        drug_narcotic_offenses=row['Drug/Narcotic Offenses'],
        gambling_offenses=row['Gambling Offenses'],
        pornography_obscene_material=row['Pornography/Obscene Material'],
        prostitution_offenses=row['Prostitution Offenses'],
        weapon_law_violations=row['Weapon Law Violations'],
        state_id=row['state_id']
        ))
    
def seed_crime_society():
    for crime_society in crime_society_list:
        db.session.add(crime_society)
        db.session.commit()

def undo_crime_society():
    for crime_society in crime_society_list():
        db.session.delete(crime_society)
        db.session.commit()



