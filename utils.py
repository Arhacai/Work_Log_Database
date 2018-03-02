import datetime
import os


def clear_screen():
    """Clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_name():
    """Gets the name of the employee from user"""
    clear_screen()
    while True:
        name = input("Employee's Name: ").strip()
        if name != '':
            return name
        else:
            print("Sorry, you must provide a name.\n")


def get_task():
    """Gets the title of the task from user"""
    clear_screen()
    while True:
        task = input("Title of the task: ")
        if task != '':
            return task
        else:
            print("Sorry, you must provide a task title.\n")


def get_time():
    """Gets a valid time spent from user"""
    clear_screen()
    while True:
        try:
            time = round(int(input("Time spent (rounded minutes): ")))
            if time <= 0:
                raise ValueError
        except ValueError:
            print("Sorry, you must enter a valid numeric time\n")
        else:
            return time


def get_notes():
    """Gets notes for the task from user (Optional)"""
    clear_screen()
    notes = input("Notes (Optional, you can leave this empty): ").strip()
    return notes


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
