from app.models import db, State


State = pd.read_csv('state_df.csv')

State_list = []

for index, row in State.iterrows():
    # State,State Code
    State_list.append(State(
        state=row['State'],
        state_code=row['State Code']
        ))
    
def seed_state():
    for state in State_list:
        db.session.add(state)
        db.session.commit()

def undo_state():
    for state in State.query.all():
        db.session.delete(state)
        db.session.commit()
    