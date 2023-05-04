from app.models import db, State
import pandas as pd
import os

csv_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '', 'state_df.csv')

state_df = pd.read_csv(csv_file_path)

State_list = []

for index, row in state_df.iterrows():
    # State,State Code
    State_list.append(State(
        state=row['State'],
        ))
    
def seed_state():
    for state in State_list:
        db.session.add(state)
        db.session.commit()

def undo_state():
    for state in State.query.all():
        db.session.delete(state)
        db.session.commit()
    