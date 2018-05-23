import sqlite3
from sqlalchemy import *

db = create_engine('sqlite:///valve.db')
db.echo = False  # Try changing this to True and see what happens

metadata = MetaData(db)

pumps = Table('valves', metadata,
    Column('valve_1_activated', Integer),
    Column('valve_1_deactivated', Integer),
    Column('valve_2_activated', Integer),
    Column('valve_2_deactivated', Integer),
    Column('valve_3_activated', Integer),
    Column('valve_3_deactivated', Integer),
    Column('valve_4_activated', Integer),
    Column('valve_4_deactivated', Integer)
)
pumps.create()
