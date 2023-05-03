from app.models import db, Business, BusinessDetail, CrimesVsPerson, CrimesVsProperty, CrimesVsSociety, State
import pandas as pd

BusinessDetail = pd.read_csv('business_details.csv')

BusinessDetail_list = []

for index, row in BusinessDetail.iterrows():
    # id,chain,independent,future
    BusinessDetail_list.append(BusinessDetail(
        id=row['id'],
        chain=row['chain'],
        independent=row['independent'],
        future=row['future']
        ))
    
def seed_business_details():
    for business_detail in BusinessDetail_list:
        db.session.add(business_detail)
        db.session.commit()

def undo_business_details():
    for business_detail in BusinessDetail.query.all():
        db.session.delete(business_detail)
        db.session.commit()
