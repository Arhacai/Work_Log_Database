import datetime
import utils
from peewee import *  # noqa (Added after peewee lines to avoid flake8 issues)

db = SqliteDatabase('employees.db')  # noqa


class BaseModel(Model):  # noqa
    class Meta:
        database = db


class Employee(BaseModel):
    name = CharField(max_length=50, unique=True)  # noqa

    def __str__(self):
        return self.name.capitalize()

    def edit(self):
        self.name = utils.get_name(self.name)
        self.save()


class Task(BaseModel):
    """Model for an employee entry. Stores in database info about an employee
    and let the user add, edit, delete and show that info.
    """
    employee = ForeignKeyField(Employee, related_name='tasks')  # noqa
    title = CharField(max_length=255)  # noqa
    date = DateTimeField(default=datetime.date.today)  # noqa
    time = IntegerField()  # noqa
    notes = TextField(default='')  # noqa

    def __str__(self):
        return "{}: {}".format(self.employee.name, self.title)

    def show(self):
        """Displays on screen the info for an entry"""
        utils.clear_screen()
        print(self.employee)
        print("="*len(self.employee.name))
        print("Date: {}".format(self.date.strftime('%d/%m/%Y')))
        print("Task: {}".format(self.title))
        print("Time spent: {} minutes".format(self.time))
        if self.notes:
            print("Notes: {}".format(self.notes))
        print()

    def edit(self):
        self.show()
        print("EDIT entry (Leave fields blank for no changes)")
        self.title = utils.get_title(self.title)
        self.date = utils.get_date(self.date)
        self.time = utils.get_time(self.time)
        self.notes = utils.get_notes(self.notes)
        self.save()


class MenuOptionModel(BaseModel):
    key = CharField(max_length=5)
    name = CharField(max_length=100)
    menu = CharField(max_length=50)
    module = CharField(max_length=50)
    obj = CharField(max_length=50)
    func = CharField(max_length=50)

    def get_obj(self):
        return getattr(__import__(str(self.module)), str(self.obj))

    def get_func(self, *args):
        return getattr(self.get_obj()(*args), str(self.func))

    def __str__(self):
        """Returns a basic display of the option. Example: a) First Option"""
        return "{}) {}".format(self.key, self.name)


def initialize():
    """Create the database and the table if they don't exist."""
    try:
        db.connect()
    except OperationalError:
        db.close()
    finally:
        db.connect()
        db.create_tables([Employee, MenuOptionModel, Task], safe=True)
