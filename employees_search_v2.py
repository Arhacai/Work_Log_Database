import utils_v2
from employees_v2 import Employee, Task


class TaskSearch:
    """Extends functionality of Employee by adding some methods to search
    entries from the database. The search methods are the follows:
    - Search by employee name
    - Search by date of task
    - Search by range of dates
    - Search by time spent
    - Search by term
    """
    @classmethod
    def search_name(cls):
        """Search by Employee Name"""
        entries = Task.select().where(Task.employee.name == utils_v2.get_name())
        return entries

    @classmethod
    def search_date(cls):
        """Search by Date of Task"""
        date = utils_v2.get_date()
        entries = Task.select().where(Task.date.year == date.year, Task.date.month == date.month, Task.date.day == date.day).order_by(Task.date)
        return entries

    @classmethod
    def search_by_range(cls):
        """Search by Range of Dates"""
        start_date, end_date = utils_v2.get_date_range()
        entries = Task.select().where(Task.date.between(start_date, end_date)).order_by(Task.date)
        return entries

    @classmethod
    def search_time(cls):
        """Search by Time Spent"""
        entries = Task.select().where(Task.time == utils_v2.get_time()).order_by(Task.date)
        return entries

    @classmethod
    def search_term(cls):
        """Search by Search Term"""
        term = utils_v2.get_term()
        entries = Task.select().where(Task.title.contains(term) | Task.notes.contains(term)).order_by(Task.date)
        return entries
