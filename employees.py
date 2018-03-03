import datetime
import utils

from peewee import *


db = SqliteDatabase('employees.db')


class Employee(Model):
    """Model for an employee entry. Stores in database info about an employee
    and let the user add, edit, delete and show that info.
    """
    date = DateTimeField(default=datetime.datetime.now)
    name = CharField(max_length=255)
    task = TextField()
    time = IntegerField()
    notes = TextField(default='')

    class Meta:
        database = db

    @classmethod
    def initialize(cls):
        """Create the database and the table if they don't exist."""
        try:
            db.connect()
        except OperationalError:
            db.close()
            db.connect()
        else:
            db.create_tables([Employee], safe=True)
        return True

    @classmethod
    def add_entry(cls, name, task, time, notes=''):
        """Add new entry"""
        Employee.create(name=name, task=task, time=time, notes=notes)
        return True

    @classmethod
    def edit_entry(cls, entry):
        """Edit entry"""
        utils.change_info(entry)
        entry.save()
        return entry

    @classmethod
    def delete_entry(cls, entry):
        """Delete a task for the user selected."""
        entry.delete_instance()
        return True

    def show_entry(self):
        """Displays on screen the info for an entry"""
        utils.clear_screen()
        print("{}".format(self.name))
        print("="*len(self.name))
        print("\nDate: {}".format(self.date.strftime('%d/%m/%Y')))
        print("Task: {}".format(self.task))
        print("Time spent: {} minutes".format(self.time))
        if self.notes != '':
            print("Notes: {}\n".format(self.notes))
        return True
