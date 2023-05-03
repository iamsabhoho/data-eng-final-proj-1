from flask.cli import AppGroup

# from .future50 import seed_future50, undo_future50
# from .independence100 import seed_independence100, undo_independence100

from .business import seed_business, undo_business
from .business_details import seed_business_details, undo_business_details
from .state import seed_states, undo_states
from .crime_property import seed_crime_property, undo_crime_property
from .crime_person import seed_crime_person, undo_crime_person
from .crime_society import seed_crime_society, undo_crime_society


seed_commands = AppGroup('seed')

# Creates the `flask seed all` command
# So we can type `flask seed all`
@seed_commands.command('all')
def seed():
    seed_business()
    seed_business_details()
    seed_states()
    seed_crime_property()
    seed_crime_person()
    seed_crime_society()
    # seed_future50()
    # seed_independence100()
    # Add other seed functions here
  

# Creates the `flask seed undo` command
# So we can type `flask seed undo`
@seed_commands.command('undo')
def undo():
    # undo_future50()
    # undo_independence100()
    undo_business()
    undo_business_details()
    undo_states()
    undo_crime_property()
    undo_crime_person()
    undo_crime_society()
    # Add other undo functions here