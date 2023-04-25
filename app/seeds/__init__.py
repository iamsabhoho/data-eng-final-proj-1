from flask.cli import AppGroup

from .future50 import seed_future50, undo_future50
from .independence100 import seed_independence100, undo_independence100


seed_commands = AppGroup('seed')

# Creates the `flask seed all` command
# So we can type `flask seed all`
@seed_commands.command('all')
def seed():
    seed_future50()
    seed_independence100()
    # Add other seed functions here

# Creates the `flask seed undo` command
# So we can type `flask seed undo`
@seed_commands.command('undo')
def undo():
    undo_future50()
    undo_independence100()
    # Add other undo functions here