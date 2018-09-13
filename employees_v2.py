import datetime
import utils

from peewee import *

import utils_v2

db = SqliteDatabase('employees_v2.db')


class Employee(Model):
    name = CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name.capitalize()

    def edit(self):
        self.name = utils_v2.get_name(self.name)
        self.save()

    class Meta:
        database = db


class Task(Model):
    """Model for an employee entry. Stores in database info about an employee
    and let the user add, edit, delete and show that info.
    """
    employee = ForeignKeyField(Employee, on_delete='CASCADE', related_name='tasks')
    title = CharField(max_length=255)
    date = DateTimeField(default=datetime.date.today)
    time = IntegerField()
    notes = TextField(default='')

    class Meta:
        database = db

    def show(self):
        """Displays on screen the info for an entry"""
        utils.clear_screen()
        print(self.employee)
        print("="*len(self.employee.name))
        print("\nDate: {}".format(self.date.strftime('%d/%m/%Y')))
        print("Task: {}".format(self.title))
        print("Time spent: {} minutes".format(self.time))
        if self.notes:
            print("Notes: {}\n".format(self.notes))
        print()

    def edit(self):
        self.show()
        print("EDIT entry (Leave fields blank for no changes)")
        self.title = utils_v2.get_title(self.title)
        self.date = utils_v2.get_date(self.date)
        self.time = utils_v2.get_time(self.time)
        self.notes = utils_v2.get_notes(self.notes)
        self.save()
