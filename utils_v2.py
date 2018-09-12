import datetime
import os

from employees_v2 import Task


def clear_screen():
    """Clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_name(initial=None):
    """Gets the name of the employee from user"""
    if not initial:
        clear_screen()
    while True:
        name = input("Employee's Name: ").strip()
        if name != '':
            return name
        if initial:
            return initial
        print("Sorry, you must provide a name.\n")


def get_title(initial=None):
    """
    Gets a valid title from user. If no title provided, it returns
    the initial title or None.
    """
    if not initial:
        clear_screen()
    while True:
        title = input("Title of the task: ")
        if title != '':
            return title
        if initial:
            return initial
        print("Sorrry, you must provide a task title")


def get_date():
    """Ask the user to provide a date to search"""
    clear_screen()
    tasks = Task.select().order_by(Task.date).distinct()
    date_list = [task.date.strftime('%d/%m/%Y') for task in tasks]
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


def get_date_range():
    """
    Gets a valid date from user. If no date provided, it returns
    the initial date or None.
    """
    clear_screen()
    while True:
        print("Enter the start date")
        start_date = input("Please use DD/MM/YYYY: ")
        try:
            start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        except ValueError:
            print("Sorry, you must enter a valid date.\n")
        else:
            break

    while True:
        print("Enter the end date")
        end_date = input("Please use DD/MM/YYYY: ")
        try:
            end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
        except ValueError:
            print("Sorry, you must enter a valid date.\n")
        else:
            return start_date.date(), end_date.date()


def get_time(initial=None):
    """
    Gets a valid time spent from user. If no time provided, it returns
    the initial time spent or None.
    """
    if not initial:
        clear_screen()
    while True:
        time = input("Time spent (rounded minutes): ")
        if time == '' and initial:
            return initial
        try:
            time = round(int(time))
            if time <= 0:
                raise ValueError
        except ValueError:
            print("Sorry, you must enter a valid numeric time")
        else:
            return time


def get_notes(initial=None):
    """
    Gets notes from user. If no notes provided, it returns the initial
    notes or None.
    """
    if not initial:
        clear_screen()
    notes = input("Notes (Optional, you can leave this empty): ").strip()
    if notes:
        return notes
    return ''


def get_term():
    """Asks the user to provide a search term in tasks/notes and returns it"""
    clear_screen()
    term = input("Enter a string to search in task name or notes: ").strip()
    return term


def change_date(entry):
    """Lets the user to change the date of the task Returns the actual
    value of the date if left blank.
    """
    while True:
        print("New date:")
        date = input("Please use DD/MM/YYY: ")
        if date == '':
            return entry.date
        else:
            try:
                date = datetime.datetime.strptime(date, '%d/%m/%Y')
            except ValueError:
                print("Sorry, you must enter a valid date.\n")
            else:
                return date


def change_task(entry):
    """Lets the user to change the title of the task. Returns the actual
    value of the task title if left blank.
    """
    task = input("Title of the task: ")
    if task != '':
        return task
    else:
        return entry.task


def change_time(entry):
    """Lets the user to change the time spent on the task. Returns the actual
    value of the time spent if left blank.
    """
    while True:
        time = input("New time spent (rounded minutes): ")
        if time == '':
            return entry.time
        else:
            try:
                time = round(int(time))
                if time <= 0:
                    raise ValueError
            except ValueError:
                print("Sorry, you must enter a valid numeric time")
            else:
                return time


def change_notes(entry):
    """Lets the user to change the task's notes. Returns the actual value of
    the task's notes if left blank.
    """
    notes = input("Notes (Optional, you can leave this empty): ").strip()
    if notes != '':
        return notes
    else:
        return entry.notes


def change_info(entry):
    """Changes date, task, time and notes of the selected entry and returns
    the modified one.
    """
    entry.show_entry()
    entry.date = change_date(entry)
    entry.task = change_task(entry)
    entry.time = change_time(entry)
    entry.notes = change_notes(entry)
    return entry
