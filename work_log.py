import models
import utils
from menu import MainMenu


class WorkLog:
    """WorkLog is a terminal application for logging what work someone did on a
    certain day. It holds a list of tasks, let the user to add, edit or delete
    any of them aswell several ways to search through the tasks. It stores this
    info on a database.
    """

    def __init__(self):
        """Create the database and the table if they don't exist."""
        models.initialize()

    def add_task(self):
        """Add new entry"""
        employee, _ = models.Employee.get_or_create(name=utils.get_name())
        task = models.Task.create(
            employee=employee,
            title=utils.get_title(),
            time=utils.get_time(),
            notes=utils.get_notes()
        )
        task.show()
        input("The entry has been added. Press enter to return to the menu")

    def edit_task(self, index, tasks):
        """Edit entry"""
        tasks[index].edit()
        return index

    def delete_task(self, index, tasks):
        """Delete a task for the user selected."""
        answer = input("Do you really want to delete this task? [y/N]: ")
        if answer.lower() == 'y':
            tasks[index].delete_instance()
            tasks.remove(tasks[index])
            if index > 1:
                return index - 1
            return 0
        return index


if __name__ == '__main__':
    MainMenu().run()
