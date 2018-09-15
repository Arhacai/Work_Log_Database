import utils
from models import Task, Employee


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
    def search_by_name(cls):
        """Search by Employee Name"""
        employee = Employee.get(Employee.name == utils.get_search_name())
        entries = employee.tasks.order_by(Task.date)
        return [entry for entry in entries]

    @classmethod
    def search_by_date(cls):
        """Search by Date of Task"""
        date = utils.get_search_date()
        entries = Task.select().where(
            Task.date.year == date.year,
            Task.date.month == date.month,
            Task.date.day == date.day
        ).order_by(Task.date)
        return [entry for entry in entries]

    @classmethod
    def search_by_range(cls):
        """Search by Range of Dates"""
        start_date, end_date = utils.get_date_range()
        entries = Task.select().where(
            Task.date.between(start_date, end_date)
        ).order_by(Task.date)
        return [entry for entry in entries]

    @classmethod
    def search_by_time(cls):
        """Search by Time Spent"""
        entries = Task.select().where(
            Task.time == utils.get_time()
        ).order_by(Task.date)
        return [entry for entry in entries]

    @classmethod
    def search_by_term(cls):
        """Search by Search Term"""
        term = utils.get_term()
        entries = Task.select().where(
            Task.title.contains(term) | Task.notes.contains(term)
        ).order_by(Task.date)
        return [entry for entry in entries]
