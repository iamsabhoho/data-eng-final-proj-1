from app.models import db, Business, BusinessDetail, CrimesVsPerson, CrimesVsProperty, CrimesVsSociety, State
import pandas as pd

crime_person = pd.read_csv('crime_person.csv')

crime_person_list = []

for index, row in crime_person.iterrows():
    #Columns: Assault Offenses,Homicide Offenses,Human Trafficking,Kidnapping/ Abduction,Sex Offenses,state_id
    
    crime_person_list.append(crime_person(
        assault_offenses=row['Assault Offenses'],
        homicide_offenses=row['Homicide Offenses'],
        human_trafficking=row['Human Trafficking'],
        kidnapping_abduction=row['Kidnapping/ Abduction'],
        sex_offenses=row['Assault Offenses'],
        state_id=row['state_id']
        ))
    
def seed_crime_person():
    for crime_person in crime_person_list:
        db.session.add(crime_person)
        db.session.commit()

def undo_crime_person():
    for crime_person in crime_person_list():
        db.session.delete(crime_person)
        db.session.commit()
