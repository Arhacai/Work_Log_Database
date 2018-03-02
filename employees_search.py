from employees import Employee

import datetime
import utils


class EmployeeSearch(Employee):
    """Extends functionality of Employee by adding some methods to search
    entries from the database. The search methods are the follows:
    - Search by employee name
    - Search by date of task
    - Search by range of dates
    - Search by time spent
    - Search by term
    """
    @classmethod
    def search_name(cls, name):
        """Search by Employee Name"""
        entries = Employee.select().where(Employee.name == name)
        show_entries(entries)
        return True

    @classmethod
    def search_date(cls, date):
        """Search by Date of Task"""
        entries = Employee.select().where(
            Employee.date.year == date.year,
            Employee.date.month == date.month,
            Employee.date.day == date.day)
        show_entries(entries)
        return True

    @classmethod
    def search_by_range(cls, *args):
        """Search by Range of Dates"""
        start_date, end_date = args
        entries = Employee.select().where(
            Employee.date.between(start_date, end_date))
        show_entries(entries)
        return True

    @classmethod
    def search_time(cls, time):
        """Search by Time Spent"""
        entries = Employee.select().where(Employee.time == time)
        show_entries(entries)
        return True

    @classmethod
    def search_term(cls, term):
        """Search by Search Term"""
        entries = Employee.select().where(
            Employee.task.contains(term) |
            Employee.notes.contains(term))
        show_entries(entries)
        return True


def show_entries(entries, index=0):
    """Displays on screen all the entries found, one at a time, with the
    ability to stop paging through records. Entries can be edited or deleted
    aswell.
    """
    entries = [entry for entry in entries]
    choice = None

    while choice != 'r':
        entries = sort_entries(entries)
        utils.clear_screen()

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


def sort_entries(entries):
    """Takes the list of entries and sort them by date (ascending)"""
    for i in range(1, len(entries)):
        j = i-1
        key = entries[i]
        while (entries[j].date > key.date) and (j >= 0):
            entries[j+1] = entries[j]
            j -= 1
        entries[j+1] = key
    return entries


def get_name_list():
    """Ask the user to provide a name to search and returns it"""
    utils.clear_screen()
    employees = Employee.select().order_by(Employee.name)
    name_list = set()
    for employee in employees:
        name_list.update([employee.name])
    name_list = list(name_list)
    name_list.sort()
    print("List of employees:")
    print("==================")
    for name in name_list:
        print("- {}".format(name))
    while True:
        name = input("\nEnter an employee name to view entries: ").strip()
        if name != '':
            return name


def get_name(name):
    """Checks if there is more than one employee with the name provided and
    if that's the case, asks the user to provide a full name again from one
    of the list and returns it. If there is no employees that match that name
    it returns it.
    """
    employees = Employee.select().where(Employee.name.contains(name))
    if employees:
        name_list = set([employees[0].name])
        for employee in employees:
            name_list.update([employee.name])
        if len(name_list) > 1:
            utils.clear_screen()
            print("List of employees that matches your search:")
            print("===========================================")
            for name in name_list:
                print("- {}".format(name))
            while True:
                name = input(
                    "\nChoose from one of these to view entries: ").strip()
                if name != '':
                    return name
                else:
                    print("Sorry, you must choose a name from the list")
        elif len(name_list) == 1:
            return name
    else:
        return name


def get_date():
    """Ask the user to provide a date to search"""
    utils.clear_screen()
    employees = Employee.select().order_by(Employee.date)
    date_list = set()
    for employee in employees:
        date_list.update([employee.date.strftime('%d/%m/%Y')])
    date_list = list(date_list)
    date_list.sort()
    print("Dates with tasks:")
    print("=================")
    for date in date_list:
        print("- {}".format(date))

    while True:
        date = input("\nEnter a date to view its entries: ").strip()
        if date == '':
            print("Sorry, you must enter a valid date.")
        else:
            try:
                date = datetime.datetime.strptime(date, '%d/%m/%Y')
            except ValueError:
                print("Sorry, you must enter a valid date.\n")
            else:
                return date


def get_start_date():
    utils.clear_screen()
    """Asks the user to provide a start date with the valid format and
    returns it."""
    while True:

        print("Enter the start date")
        start_date = input("Please use DD/MM/YYYY: ")
        try:
            start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        except ValueError:
            print("Sorry, you must enter a valid date.\n")
        else:
            return start_date


def get_end_date():
    """Asks the user to provide an end date with the valid format and
    returns it."""
    while True:
        print("\nEnter the end date")
        end_date = input("Please use DD/MM/YYYY: ")
        try:
            end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
        except ValueError:
            print("Sorry, you must enter a valid date.\n")
        else:
            return end_date


def get_time():
    """Asks the user to provide a valid numeric integer time and returns it"""
    utils.clear_screen()
    while True:
        try:
            time = round(int(input("Enter time spent(rounded minutes): ")))
            if time <= 0:
                raise ValueError
        except ValueError:
            print("Sorry, you must enter a valid numeric time.\n")
        else:
            return time


def get_term():
    """Asks the user to provide a search term in tasks/notes and returns it"""
    utils.clear_screen()
    term = input("Enter a string to search in task name or notes: ").strip()
    return term
