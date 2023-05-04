from app.models import db, Business, BusinessDetail, CrimesVsPerson, CrimesVsProperty, CrimesVsSociety, State
import pandas as pd
import os

csv_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '', 'business_df.csv')


business_df = pd.read_csv(csv_file_path)

Business_list = []

for index, row in business_df.iterrows():
    #id, Restaurant,Sales,City,State,YOY_Sales,state_id, business_id
    business = Business(
        restaurant=row['Restaurant'],
        sales=row['Sales'],
        city=row['City'],
        state=row['State'],
        yoy_sales=row['YOY_Sales'],
        state_id=row['state_id'],  
    )
    Business_list.append(business)
    
    
def seed_business():
    for business in Business_list:
        db.session.add(business)
        db.session.commit()

def undo_business():
    for business in Business.query.all():
        db.session.delete(business)
        db.session.commit()
    