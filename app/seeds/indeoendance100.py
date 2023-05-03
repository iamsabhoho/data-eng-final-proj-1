from app.models import db, Future50, Independence100
import pandas as pd

independance = pd.read_csv('Independence100.csv')

independance_list = []

for index, row in independance.iterrows():
    # Rank	Restaurant	Sales	Average Check	City	State	Meals_Served
    independance_list.append(Independence100(
        rank=row['Rank'],
        restaurant=row['Restaurant'],
        sales=row['Sales'],
        average_check=row['Average Check'],
        city=row['City'],
        state=row['State'],
        meals_served=row['Meals Served']
        ))
    
def seed_independence100():
    for independance in independance_list:
        db.session.add(independance)
        db.session.commit()

def undo_independence100():
    for independance in independance_list():
        db.session.delete(independance)
        db.session.commit()