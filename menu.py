import utils
from search import TaskSearch
from models import Task, MenuOptionModel


class MenuOption:
    """
    This class lets the creation of menu options, holding information about
    how they are displayed, and how to operate over other classes, functions
    or methods.
    """
    def __init__(self, key, name, obj, func, *params):
        """
        Initializes a menu option with needed attributes
        :param key: The keyword that represent the option
        :param name: The name that is going to be displayed alongside the key
        :param obj: The object or class to be called with the option
        :param func: The function or method to be executed
        :param params: Any params the function could have to be called with
        """
        self.key = key
        self.name = name
        self.obj = obj
        self.func = func
        self.params = params

    def __str__(self):
        """Returns a basic display of the option. Example: a) First Option"""
        return "{}) {}".format(self.key, self.name)


class Menu:
    """
    Base class to create menus with a set of options given. It shows the menu
    title and its options on screen, waits for a valid user choice and
    execute the function provided by the option until selected exit option.
    """
    options = []

    def print_title(self):
        """Prints the menu header. Must be implemented on child classes"""
        raise NotImplementedError()

    def print_options(self):
        """Prints the list of menu options"""
        for option in self.options:
            print(option)

    def print_menu(self):
        """Prints the whole menu on screen: Title and Options"""
        utils.clear_screen()
        self.print_title()
        self.print_options()

    def get_option(self):
        """
        Gets the user's choice. If its not in the list of keys from the
        option list, it displays an error and repeat again until a valid one
        is provided
        """
        while True:
            choice = input("> ")
            for option in self.options:
                if choice == option.key:
                    return option
            print("Sorry, you must choose a valid option")

    def get_function(self, option, *args):
        """
        Returns the result of the option chosen, executed with the proper
        params if provided and needed for the execution.
        """
        return option.get_func(*args)

    def run(self, *args):
        """
        Runs de menu. Display all info on screen, gets the user's choice
        and execute the option. It keeps looping until quit method is called.
        If a menu needs to do something with the result of the execuction of
        the option, it can be done overriding the side_run method.
        """
        while True:
            self.print_menu()
            result = self.get_function(self.get_option())(*args)
            if isinstance(result, MenuOptionModel):
                break
            self.side_run(result)

    def side_run(self, result):
        """
        Extra functionality for the run method. Any code here will be run
        after the option chosen finish its work. By default this does nothing.
        """
        pass

    @staticmethod
    def quit(*args):
        """
        Extra method provided to quit the actual menu. It should be included
        as the last option of the menu.
        """
        return MenuOptionModel()


class MainMenu(Menu):
    """
    Main menu of the Work Log application. It lets the user to create a new
    entry, to search in existing entries or to quit program.
    """

    def __init__(self):
        """
        Initializes the menu with a WorkLog object. It also creates three
        menu options to show and to operate with.
        """
        self.options = [
            MenuOptionModel.get_or_create(
                key='a',
                name='Add new entry',
                menu='MainMenu',
                module='work_log',
                obj='WorkLog',
                func='add_task'
            )[0],
            MenuOptionModel.get_or_create(
                key='b',
                name='Search in existing entries',
                menu='MainMenu',
                module='menu',
                obj='SearchMenu',
                func='run'
            )[0],
            MenuOptionModel.get_or_create(
                key='c',
                name='Quit program',
                menu='MainMenu',
                module='menu',
                obj='MainMenu',
                func='quit'
            )[0]
        ]

    def print_title(self):
        """Main Menu header"""
        print("WORK LOG")
        print("What would you like to do?")


class SearchMenu(Menu, TaskSearch):
    """
    Search menu of the WorkLog application. It lets the user to search in
    entries using several methods provided by the TaskSearch class.
    """

    def __init__(self):
        """
        Initializes the menu with a WorkLog object. It also creates six
        menu options to show and to operate with.
        """
        self.options = [
            MenuOptionModel.get_or_create(
                key='a',
                name='Employee Name',
                menu='SearchMenu',
                module='menu',
                obj='SearchMenu',
                func='search_by_name'
            )[0],
            MenuOptionModel.get_or_create(
                key='b',
                name='Date of Task',
                menu='SearchMenu',
                module='menu',
                obj='SearchMenu',
                func='search_by_date'
            )[0],
            MenuOptionModel.get_or_create(
                key='c',
                name='Range of Dates',
                menu='SearchMenu',
                module='menu',
                obj='SearchMenu',
                func='search_by_range'
            )[0],
            MenuOptionModel.get_or_create(
                key='d',
                name='Time Spent',
                menu='SearchMenu',
                module='menu',
                obj='SearchMenu',
                func='search_by_time'
            )[0],
            MenuOptionModel.get_or_create(
                key='e',
                name='Search Term',
                menu='SearchMenu',
                module='menu',
                obj='SearchMenu',
                func='search_by_term'
            )[0],
            MenuOptionModel.get_or_create(
                key='f',
                name='Return to menu',
                menu='SearchMenu',
                module='menu',
                obj='SearchMenu',
                func='quit'
            )[0]
        ]

    def print_title(self):
        """Search Menu header"""
        print("Do you want to search by:")

    def side_run(self, result):
        """After the option chosen returns a list of tasks, they must be shown
        creating a TaskMenu object to display them."""
        TaskMenu(0, result).run()


class TaskMenu(Menu):
    """
    Task menu of the WorkLog application. It lets the user to see, edit or
    delete any of the tasks shown one at a time. Menu lets user to pass through
    tasks back and forth.
    """

    def __init__(self, index=0, tasks=None):
        """
        Initializes the menu with a WorkLog object. By default, index is 0
        so the first task in the list is shown. If no tasks provided, this
        menu gets all tasks from the log and shows them. It also creates five
        menu options to show and operate with. Menu options are different
        depending on the index of the task shown, so options are changed
        on __init__ in each case.
        """
        self.index = index
        if tasks is None:
            self.tasks = [entry for entry in Task.select().order_by(Task.date)]
        else:
            self.tasks = tasks
        self.options = [
            MenuOptionModel.get_or_create(
                key='p',
                name='[P]revious',
                menu='TaskMenu',
                module='menu',
                obj='TaskMenu',
                func='previous_task'
            )[0],
            MenuOptionModel.get_or_create(
                key='n',
                name='[N]ext',
                menu='TaskMenu',
                module='menu',
                obj='TaskMenu',
                func='next_task'
            )[0],
            MenuOptionModel.get_or_create(
                key='e',
                name='[E]dit',
                menu='TaskMenu',
                module='work_log',
                obj='WorkLog',
                func='edit_task'
            )[0],
            MenuOptionModel.get_or_create(
                key='d',
                name='[D]elete',
                menu='TaskMenu',
                module='work_log',
                obj='WorkLog',
                func='delete_task'
            )[0],
            MenuOptionModel.get_or_create(
                key='r',
                name='[R]eturn',
                menu='TaskMenu',
                module='menu',
                obj='TaskMenu',
                func='quit'
            )[0],
        ]
        self.options = self.get_options(index, len(self.tasks))

    def get_options(self, index, length):
        """
        Return a list of available options to show in the menu depending
        on the index of the task and the lenght of tasks.
        """
        if length == 0:
            return [self.options[-1]]
        if index == 0:
            if length == 1:
                return self.options[2:]
            return self.options[1:]
        if index == length - 1:
            return [self.options[0]] + self.options[2:]
        if index >= length:
            raise IndexError("list index out of range")
        return self.options

    def print_title(self):
        """Task Menu header"""
        if self.tasks:
            self.tasks[self.index].show()
            print("Result {} of {}\n".format(self.index + 1, len(self.tasks)))
        else:
            print("There are no tasks to show.\n")

    def print_options(self):
        """Prints menu options in a different way than the base menu class"""
        print(', '.join([option.name for option in self.options]))

    def run(self, *args):
        """
        Runs de menu. Display all info on screen, gets the user's choice
        and execute the option. It keeps looping until quit method is called.
        If a menu needs to do something with the result of the execuction of
        the option, it can be done overriding the side_run method.
        """
        while True:
            self.print_menu()
            result = self.get_function(self.get_option(), self.index, self.tasks)(*args)
            if isinstance(result, MenuOptionModel):
                break
            self.side_run(result)

    def side_run(self, result):
        """
        Upon completion of option chosen, index is updated to show the proper
        task on next iteration of the menu.
        """
        self.index = result
        self.__init__(self.index, self.tasks)

    def previous_task(self, *args):
        """Decreases index by one to show previous task"""
        return self.index - 1

    def next_task(self, *args):
        """Increases index by one to show next task"""
        return self.index + 1
