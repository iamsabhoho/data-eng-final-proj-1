from app.models import db, Business, BusinessDetail, CrimesVsPerson, CrimesVsProperty, CrimesVsSociety, State
import pandas as pd

Business = pd.read_csv('business_df.csv')

Business_list = []

for index, row in Business.iterrows():
    #id, Restaurant,Sales,City,State,YOY_Sales,state_id, business_id
    Business_list.append(Business(
        id=row['id'],
        restaurant=row['Restaurant'],
        sales=row['Sales'],
        city=row['City'],
        yoy_sales=row['YOY_Sales'],
        state_id=row['state_id'],
        business_id=row['business_id']
        ))
    
def seed_business():
    for business in Business_list:
        db.session.add(business)
        db.session.commit()

def undo_business():
    for business in Business.query.all():
        db.session.delete(business)
        db.session.commit()
    