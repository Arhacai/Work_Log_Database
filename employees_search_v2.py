import utils_v2
from employees_v2 import Employee, Task


class Search:

    @classmethod
    def sort_entries(cls, entries):
        """Takes the list of entries and sort them by date (ascending)"""
        for i in range(1, len(entries)):
            j = i - 1
            key = entries[i]
            while (entries[j].date > key.date) and (j >= 0):
                entries[j + 1] = entries[j]
                j -= 1
            entries[j + 1] = key
        return entries


class EmployeeSearch(Search):

    def __init__(self):
        self.employees = Employee.select().order_by(Employee.name)
        self.name = self.get_name()

    def search_name(self):
        """Search by Employee Name"""
        entries = Task.select().where(employee__name=self.name)
        return self.sort_entries(entries)

    def get_name(self):
        utils_v2.clear_screen()
        print("List of employees:")
        print("==================")
        for employee in self.employees:
            print("- {}".format(employee.name))
        employees = self.get_employee_name()
        while len(employees) > 1:
            utils_v2.clear_screen()
            print("Two or more employees matches your search:")
            print("==========================================")
            for employee in employees:
                print("- {}".format(employee.name))
                employees = self.get_employee_name()
        if len(employees) == 1:
            return employees[0].name
        return ''

    @staticmethod
    def get_employee_name():
        """Gets the name of the employee from user"""
        while True:
            name = input("Employee's Name: ").strip()
            entries = Employee.select().where(Employee.name.contains(name))
            if entries:
                return entries
            if name == 'q':
                break
            print("Sorry, you must provide a valid name, or 'q' to quit\n")


class TaskSearch(Search):
    """Extends functionality of Employee by adding some methods to search
    entries from the database. The search methods are the follows:
    - Search by employee name
    - Search by date of task
    - Search by range of dates
    - Search by time spent
    - Search by term
    """

    @classmethod
    def search_date(cls):
        """Search by Date of Task"""
        date = utils_v2.get_date()
        entries = Employee.select().where(
            Employee.date.year == date.year,
            Employee.date.month == date.month,
            Employee.date.day == date.day
        )
        return cls.sort_entries(entries)

    @classmethod
    def search_by_range(cls):
        """Search by Range of Dates"""
        start_date, end_date = utils_v2.get_date_range()
        entries = Employee.select().where(
            Employee.date.between(start_date, end_date))
        return cls.sort_entries(entries)

    @classmethod
    def search_time(cls):
        """Search by Time Spent"""
        entries = Employee.select().where(Employee.time == utils_v2.get_time())
        return cls.sort_entries(entries)

    @classmethod
    def search_term(cls):
        """Search by Search Term"""
        term = utils_v2.get_term()
        entries = Employee.select().where(
            Employee.task.contains(term) |
            Employee.notes.contains(term))
        return cls.sort_entries(entries)


def show_entries(entries, index=0):
    """Displays on screen all the entries found, one at a time, with the
    ability to stop paging through records. Entries can be edited or deleted
    aswell.
    """
    entries = [entry for entry in entries]
    choice = None

    while choice != 'r':
        entries = sort_entries(entries)
        utils_v2.clear_screen()

        # If search method finds no entries
        if len(entries) == 0:
            print("There are no tasks to show.\n")
            print("[R]eturn to search menu\n")
            input("> ")
            break

        # If search method finds only one entry
        elif index == 0 and len(entries) == 1:
            entries[index].show_entry()
            print("\nResult {} of {}\n".format(index+1, len(entries)))
            print("[E]dit, [D]elete, [R]eturn to search menu\n")
            choice = input("> ").lower().strip()
            if choice == 'e':
                entries[index] = Employee.edit_entry(entries[index])
            elif choice == 'd':
                if input("\nAre you sure? [y/N]: ").lower() == 'y':
                    Employee.delete_entry(entries[index])
                    del entries[index]
                    index = 0
                    print("\nEntry deleted!")
                    input("\nPress any key to continue")

        # More than one entry is found and the first one is selected
        elif index == 0 and len(entries) > 1:
            entries[index].show_entry()
            print("\nResult {} of {}\n".format(index+1, len(entries)))
            print("[N]ext, [E]dit, [D]elete, [R]eturn to search menu\n")
            choice = input("> ").lower().strip()
            if choice == 'n':
                index += 1
            elif choice == 'e':
                entries[index] = Employee.edit_entry(entries[index])
            elif choice == 'd':
                if input("\nAre you sure? [y/N]: ").lower() == 'y':
                    Employee.delete_entry(entries[index])
                    del entries[index]
                    index = 0
                    print("\nEntry deleted!")
                    input("\nPress any key to continue")

        # More than one entry is found and the selected one is in the middle
        elif index > 0 and index < len(entries)-1:
            entries[index].show_entry()
            print("\nResult {} of {}\n".format(index+1, len(entries)))
            print("""
[N]ext, [P]revious, [E]dit, [D]elete, [R]eturn to search menu\n""")
            choice = input("> ").lower().strip()
            if choice == 'n':
                index += 1
            elif choice == 'p':
                index -= 1
            elif choice == 'e':
                entries[index] = Employee.edit_entry(entries[index])
            elif choice == 'd':
                if input("\nAre you sure? [y/N]: ").lower() == 'y':
                    Employee.delete_entry(entries[index])
                    del entries[index]
                    index -= 1
                    print("\nEntry deleted!")
                    input("\nPress any key to continue")

        # More than one entry found and the selected is the last one of them
        elif index == len(entries)-1:
            entries[index].show_entry()
            print("\nResult {} of {}\n".format(index+1, len(entries)))
            print("[P]revious, [E]dit, [D]elete, [R]eturn to search menu\n")
            choice = input("> ").lower().strip()
            if choice == 'p':
                index -= 1
            elif choice == 'e':
                entries[index] = Employee.edit_entry(entries[index])
            elif choice == 'd':
                if input("\nAre you sure? [y/N]: ").lower() == 'y':
                    Employee.delete_entry(entries[index])
                    del entries[index]
                    index -= 1
                    print("\nEntry deleted!")
                    input("\nPress any key to continue")
    return True


