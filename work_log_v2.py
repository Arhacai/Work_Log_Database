from collections import OrderedDict

import utils_v2
from employees_v2 import Employee, Task
import employees_search
from employees_search import EmployeeSearch

import utils


class WorkLog():
    """WorkLog is a terminal application for logging what work someone did on a
    certain day. It holds a list of tasks, let the user to add, edit or delete
    any of them aswell several ways to search through the tasks. It stores this
    info on a database.
    """

    def __init__(self):
        """Create the database and the table if they don't exist."""
        self.initialize()

    def initialize(self):
        """Create the database and the table if they don't exist."""
        from peewee import SqliteDatabase
        db = SqliteDatabase('employees_v2.db')
        db.connect()
        db.create_tables([Employee, Task], safe=True)

    def add_task(self):
        """Add new entry"""
        employee, _ = Employee.get_or_create(name=utils_v2.get_name())
        task = Task.create(
            employee=employee,
            title=utils_v2.get_title(),
            time=utils_v2.get_time(),
            notes=utils_v2.get_notes()
        )
        task.show()
        input("The entry has been added. Press enter to return to the menu")

    def edit_task(self, task):
        """Edit entry"""
        task.edit()

    def delete_task(self, task):
        """Delete a task for the user selected."""
        answer = input("Do you really want to delete this task? [y/N]: ")
        if answer.lower() == 'y':
            task.delete_instance()

    def main_menu(self):
        """Show the main menu"""
        choice = None

        while choice != 'c':
            utils.clear_screen()
            print("WORK LOG")
            print("What would you like to do?")
            print("a) Add new entry")
            print("b) Search in existing entries")
            print("c) Quit program")

            choice = input("\n> ").lower().strip()
            if choice == 'a':
                name = utils.get_name()
                task = utils.get_task()
                time = utils.get_time()
                notes = utils.get_notes()
                Employee.add_entry(name, task, time, notes)
            elif choice == 'b':
                self.search_menu()
        return True

    def search_menu(self):
        """Search in existing entries"""
        search_menu = OrderedDict([
            ('a', EmployeeSearch.search_name),
            ('b', EmployeeSearch.search_date),
            ('c', EmployeeSearch.search_by_range),
            ('d', EmployeeSearch.search_time),
            ('e', EmployeeSearch.search_term),
        ])

        choice = None

        while choice != 'f':
            utils.clear_screen()
            print("Do you want to search by:")
            for key, value in search_menu.items():
                print("{}) {}".format(key, value.__doc__[10:]))
            print("f) Return to main menu")

            choice = input("\n> ").lower().strip()
            if choice == 'a':
                EmployeeSearch.search_name(employees_search.get_name(
                    employees_search.get_name_list()))
            if choice == 'b':
                EmployeeSearch.search_date(employees_search.get_date())
            if choice == 'c':
                EmployeeSearch.search_by_range(
                    employees_search.get_start_date(),
                    employees_search.get_end_date())
            if choice == 'd':
                EmployeeSearch.search_time(employees_search.get_time())
            if choice == 'e':
                EmployeeSearch.search_term(employees_search.get_term())
        return True


if __name__ == '__main__':
    WorkLog().main_menu()
