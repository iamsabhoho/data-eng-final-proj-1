from app.models import db, Future50, Independence100
from pands import pandas as pd

future = pd.read_csv('Future50.csv')

future_list = []

for index, row in future.iterrows():
    # Rank	Restaurant	Sales	YOY_Sales	Units	YOY_Units	Unit_Volume	Franchising	City	State
    future_list.append(Future50(
        rank=row['Rank'],
        restaurant=row['Restaurant'],
        sales=row['Sales'],
        yoy_sales=row['YOY_Sales'],
        units=row['Units'],
        yoy_units=row['YOY_Units'],
        unit_volume=row['Unit_Volume'],
        franchising=row['Franchising'],
        city=row['City'],
        state=row['State']
        ))
    
def seed_future50():
    for future in future_list:
        db.session.add(future)
        db.session.commit()

def undo_future50():
    for future in Future50.query.all():
        db.session.delete(future)
        db.session.commit()