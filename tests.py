import datetime
import employees_search
import unittest
import utils
import work_log

from employees import Employee
from employees_search import EmployeeSearch
from unittest.mock import patch
from work_log import WorkLog


class UtilsTest(unittest.TestCase):
    def setUp(self):
        Employee.initialize()
        self.entry = Employee.create(
            name='Adrian',
            task='Python Testing',
            time=10,
            notes='Testing some methods'
        )

    def test_get_name(self):
        utils.input = lambda _: 'Adrian'
        name = utils.get_name()
        self.assertEqual(name, 'Adrian')

    def test_get_task(self):
        utils.input = lambda _: 'Python Testing'
        task = utils.get_task()
        self.assertEqual(task, 'Python Testing')

    def test_get_time(self):
        utils.input = lambda _: 30
        time = utils.get_time()
        self.assertEqual(time, 30)

    def test_get_notes(self):
        utils.input = lambda _: 'Testing some methods'
        notes = utils.get_notes()
        self.assertEqual(notes, 'Testing some methods')

    def test_change_date(self):
        utils.input = lambda _: '25/02/2018'
        date = utils.change_date(self.entry).strftime('%d/%m/%Y')
        self.assertEqual(date, '25/02/2018')

    def test_change_date_no_input(self):
        utils.input = lambda _: ''
        date = utils.change_date(self.entry)
        self.assertEqual(date, self.entry.date)

    def test_change_task(self):
        utils.input = lambda _: 'New Task'
        task = utils.change_task(self.entry)
        self.assertEqual(task, 'New Task')

    def test_change_task_no_input(self):
        utils.input = lambda _: ''
        task = utils.change_task(self.entry)
        self.assertEqual(task, self.entry.task)

    def test_change_time(self):
        utils.input = lambda _: 30
        time = utils.change_time(self.entry)
        self.assertEqual(time, 30)

    def test_change_time_no_input(self):
        utils.input = lambda _: ''
        time = utils.change_time(self.entry)
        self.assertEqual(time, self.entry.time)

    def test_change_notes(self):
        utils.input = lambda _: 'Testing some methods'
        notes = utils.change_notes(self.entry)
        self.assertEqual(notes, 'Testing some methods')

    def test_change_notes_no_input(self):
        utils.input = lambda _: ''
        notes = utils.change_notes(self.entry)
        self.assertEqual(notes, self.entry.notes)

    def tearDown(self):
        self.entry.delete_instance()


class EmployeeTest(unittest.TestCase):
    def setUp(self):
        Employee.initialize()
        self.entry = Employee.create(
            name='Adrian',
            task='Python Testing',
            time='10',
            notes='Testing some methods'
        )

    def test_initialization(self):
        self.assertEqual(Employee.initialize(), True)

    def test_deletion(self):
        self.assertEqual(Employee.delete_entry(self.entry), True)

    def test_adding(self):
        new_entry = Employee.add_entry(
            name='Adrian',
            task='Learning Django',
            time='40',
            notes='Learning Django basics'
        )
        self.assertIsInstance(new_entry, Employee)
        new_entry = Employee.get(
            Employee.name == 'Adrian',
            Employee.task == 'Learning Django',
            Employee.time == 40,
            Employee.notes == 'Learning Django basics'
        )
        new_entry.delete_instance()

    def test_showing_entry(self):
        self.assertEqual(self.entry.show_entry(), True)

    def tearDown(self):
        self.entry.delete_instance()


class EmployeeSearchTest(unittest.TestCase):
    def setUp(self):
        Employee.initialize()
        self.employee = Employee.create(
            date=datetime.datetime.strptime('12/02/2018', '%d/%m/%Y'),
            name='Jackson',
            task='Python Testing',
            time='10',
            notes='Testing some methods'
        )
        self.employee_2 = Employee.create(
            date=datetime.datetime.strptime('01/05/2019', '%d/%m/%Y'),
            name='Samuel Jackson',
            task='Learning Python',
            time='50',
            notes='Learning the basics of python'
        )
        self.employee_3 = Employee.create(
            date=datetime.datetime.strptime('01/02/2017', '%d/%m/%Y'),
            name='Livja',
            task='Learning Flask',
            time='20',
            notes='Learning the basics of Flask'
        )
        self.entries = [self.employee, self.employee_2, self.employee_3]

    def test_sort_entries(self):
        self.assertLess(employees_search.sort_entries(
                        self.entries)[0].date,
                        self.entries[-1].date)

    def test_get_name_list(self):
        with unittest.mock.patch('builtins.input', return_value='Adrian'):
            self.assertEqual(employees_search.get_name_list(), 'Adrian')

    def test_get_name_shared_name(self):
        with unittest.mock.patch('builtins.input', return_value='Jackson'):
            self.assertEqual(employees_search.get_name('Jackson'), 'Jackson')

    def test_get_name_only_one(self):
        with unittest.mock.patch('builtins.input', return_value='Livja'):
            self.assertEqual(employees_search.get_name('Livja'), 'Livja')

    def test_get_date(self):
        with unittest.mock.patch('builtins.input', return_value='28/02/2018'):
            self.assertEqual(
                employees_search.get_date(),
                datetime.datetime.strptime('28/02/2018', '%d/%m/%Y')
            )

    def test_get_start_date(self):
        with unittest.mock.patch('builtins.input', return_value='20/02/2018'):
            start_date = employees_search.get_start_date()
        with unittest.mock.patch('builtins.input', return_value='25/02/2018'):
            end_date = employees_search.get_end_date()
        self.assertLess(start_date, end_date)

    def test_get_time(self):
        with unittest.mock.patch('builtins.input', return_value=10):
            self.assertEqual(employees_search.get_time(), 10)

    def test_get_term(self):
        with unittest.mock.patch('builtins.input', return_value='Notes'):
            self.assertEqual(employees_search.get_term(), 'Notes')

    def test_show_entries_first(self):
        with unittest.mock.patch('builtins.input', return_value='r'):
            self.assertTrue(employees_search.show_entries(self.entries))

    def test_show_entries_first_and_only(self):
        with unittest.mock.patch('builtins.input', return_value='r'):
            self.assertTrue(employees_search.show_entries([self.employee]))

    def test_show_entries_middle(self):
        with unittest.mock.patch('builtins.input', return_value='r'):
            self.assertTrue(employees_search.show_entries(self.entries, 1))

    def test_show_entries_last(self):
        with unittest.mock.patch('builtins.input', return_value='r'):
            self.assertTrue(employees_search.show_entries(self.entries, 2))

    def test_search_name(self):
        with unittest.mock.patch('builtins.input', return_value='r'):
            self.assertTrue(EmployeeSearch.search_name('Adrian'))

    def test_search_date(self):
        with unittest.mock.patch('builtins.input', return_value='r'):
            self.assertTrue(EmployeeSearch.search_date(
                        datetime.datetime.strptime('01/03/2018', '%d/%m/%Y')))

    def test_search_by_range(self):
        with unittest.mock.patch('builtins.input', return_value='r'):
            self.assertTrue(EmployeeSearch.search_by_range(
                        datetime.datetime.strptime('01/03/2018', '%d/%m/%Y'),
                        datetime.datetime.strptime('01/03/2018', '%d/%m/%Y')))

    def test_search_time(self):
        with unittest.mock.patch('builtins.input', return_value='r'):
            self.assertTrue(EmployeeSearch.search_time(10))

    def test_search_term(self):
        with unittest.mock.patch('builtins.input', return_value='r'):
            self.assertTrue(EmployeeSearch.search_term('Testing some methods'))

    def tearDown(self):
        self.employee.delete_instance()
        self.employee_2.delete_instance()
        self.employee_3.delete_instance()


class WorkLogTest(unittest.TestCase):

    def test_main_menu(self):
        work_log.input = lambda _: 'c'
        self.assertEqual(WorkLog().main_menu(), True)
        utils.clear_screen()

    def test_search_menu(self):
        work_log.input = lambda _: 'f'
        self.assertEqual(WorkLog().search_menu(), True)
        utils.clear_screen()


if __name__ == '__main__':
    unittest.main()
