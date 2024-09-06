from datetime import date, datetime
import unittest
import manager


@unittest.skip("Passed")
class TestAppendNRmove(unittest.TestCase):
    def setUp(self):
        self.man = manager.Manager(60, 60)

    def test_append(self):
        print("------------------ Start Of Append Test----------------------")

        self.man.add_task("task 1", date(1, 1, 2), date(1, 1, 1), "member 1")
        self.man.add_task("task 2", date(2, 2, 4), date(12, 6, 8))
        self.man.add_task("task 3", date(1, 4, 2), date(1, 8, 6), "member 3")
        print(self.man.print_all_task())

        self.man.add_meeting("first meeting", "at 123 abby-lane", datetime(12, 6, 8))
        self.man.add_meeting("second meeting", "at your mom's", datetime(12, 6, 9))
        self.man.add_meeting("third meeting", "Never", datetime(19, 10, 21))
        print(self.man.print_all_meetings())

        self.assertEqual(len(self.man.tasks), 3)
        self.assertEqual(len(self.man.meetings), 3)

        self.man.tasks = []
        self.man.meetings = []

        print("------------------ End Of Append Test----------------------")

    def test_assign(self):
        print("------------------ Start Of Assign Test----------------------")
        task1 = manager.Task("task 1", date(1, 1, 2), date(1, 1, 1), "member 2")
        task2 = manager.Task("task 2", date(2, 2, 4), date(12, 6, 8), "The New Guy")

        self.man.add_task("task 1", date(1, 1, 2), date(1, 1, 1), "member 1")
        self.man.add_task("task 2", date(2, 2, 4), date(12, 6, 8))
        print(self.man.print_all_task())

        self.man.assign_task(1, "member 2")
        self.man.assign_task(2, "The New Guy")
        print(self.man.print_all_task())

        self.assertEqual(self.man.tasks[0].assi_to, task1.assi_to)
        self.assertEqual(self.man.tasks[1].assi_to, task2.assi_to)

        self.man.tasks = []
        self.man.meetings = []
        print("---------------------- End Of Assign Test----------------------")

    def test_remove(self):
        print("------------------ Start Of Remove Test----------------------")

        self.man.add_task("task 1", date(1, 1, 2), date(1, 1, 1), "member 1")
        self.man.add_task("task 2", date(2, 2, 4), date(12, 6, 8))
        self.man.add_task("task 3", date(1, 4, 2), date(1, 8, 6), "member 3")

        self.man.add_meeting("first meeting", "at 123 abby-lane", datetime(12, 6, 8))
        self.man.add_meeting("second meeting", "at your mom's", datetime(12, 6, 9))
        self.man.add_meeting("third meeting", "Never", datetime(19, 10, 21))

        print(self.man.print_all_task())
        print(self.man.remove_task(1))
        print(self.man.remove_task(1))
        print(self.man.remove_task(1))
        print(self.man.print_all_task())

        print(self.man.print_all_meetings())
        print(self.man.remove_meeting(1))
        print(self.man.remove_meeting(1))
        print(self.man.remove_meeting(1))
        print(self.man.print_all_meetings())

        self.assertEqual(self.man.tasks, [])
        self.assertEqual(self.man.meetings, [])

        print("------------------ End Of Remove Test----------------------")


class TestBackupNRecovery(unittest.TestCase):
    def setUp(self):
        self.man = manager.Manager(1, 1)
        self.man.change_backup_time(seconds=30)
        self.man.change_reminder_time(seconds=30)

        self.man.add_task("task 1", date(1, 1, 2), date(1, 1, 1), "member 1")
        self.man.add_task("task 2", date(2, 2, 4), date(12, 6, 8))
        self.man.add_task("task 3", date(1, 4, 2), date(1, 8, 6), "member 3")

        self.man.add_meeting("first meeting", "at 123 abby-lane", datetime(12, 6, 8))
        self.man.add_meeting("second meeting", "at your mom's", datetime(12, 6, 9))
        self.man.add_meeting("third meeting", "Never", datetime(19, 10, 21))

    def test_backup(self):
        print("------------------- Start of Backup Test -----------------")
        self.man.backup()
        self.assertCountEqual(
            self.man.backup_db.execute("SELECT * FROM meetings").fetchall(),
            self.man.meetings,
        )
        self.assertCountEqual(
            self.man.backup_db.execute("SELECT * FROM tasks").fetchall(),
            self.man.tasks,
        )
        print("------------------- End of Backup Test -----------------")

    def test_recover(self):
        print("------------------- Start of Recovery Test -----------------")
        self.man.recover()
        print("------------------- End of Recovery Test -----------------")

    def tearDown(self):
        self.man.backup_db.execute("DELETE FROM meetings")
        self.man.backup_db.execute("DELETE FROM tasks")


if __name__ == "__main__":
    # TODO: make  integration test
    unittest.main()
