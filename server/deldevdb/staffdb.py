""" DelDev Staff table """

from .db import DB

class StaffDB(DB):

    def __init__(self, f=None):
        self.table_name = 'staff'

        self.columns = ['user_id', 'name', 'email', 'title']
        self.read_config(f)
