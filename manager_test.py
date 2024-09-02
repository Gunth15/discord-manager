from datetime import date, datetime
import unittest
import manager


class TestAppendNRmove(unittest.TestCase):
    def setUp(self):
        self.man = manager.Manager(60, 60)

    def test_append(self):
        task1 = manager.Task("task 1", date(1, 1, 2), date(1, 1, 1), "memeber 1")
        task2 = manager.Task("task 2", date(2, 2, 4), date(12, 6, 8), None)
        task3 = manager.Task("task 3", date(1, 4, 2), date(1, 8, 6), "memeber 3")

        meeting1 = manager.Meeting(
            "first meeting", "at 123 abby-lane", datetime(12, 6, 8)
        )
        meeting2 = manager.Meeting(
            "second meeting", "at your mom's", datetime(12, 6, 9)
        )
        meeting3 = manager.Meeting("third meeting", "Never", datetime(19, 10, 21))

        self.man.add_task("task 1", date(1, 1, 2), date(1, 1, 1), "memeber 1")
        self.man.add_task("task 2", date(2, 2, 4), date(12, 6, 8))
        self.man.add_task("task 3", date(1, 4, 2), date(1, 8, 6), "memeber 3")
        print(self.man.print_all_task())

        self.man.add_meeting("first meeting", "at 123 abby-lane", datetime(12, 6, 8))
        self.man.add_meeting("second meeting", "at your mom's", datetime(12, 6, 9))
        self.man.add_meeting("third meeting", "Never", datetime(19, 10, 21))
        print(self.man.print_all_meetings())

        self.assertEqual(self.man.tasks, [task1, task2, task3])
        self.assertEqual(self.man.meetings, [meeting1, meeting2, meeting3])

        self.man.tasks = []
        self.man.meetings = []

    def test_assign(self):
        pass

    def test_remove(self):
        self.man.add_task("task 1", date(1, 1, 2), date(1, 1, 1), "memeber 1")
        self.man.add_task("task 2", date(2, 2, 4), date(12, 6, 8))
        self.man.add_task("task 3", date(1, 4, 2), date(1, 8, 6), "memeber 3")

        self.man.add_meeting("first meeting", "at 123 abby-lane", datetime(12, 6, 8))
        self.man.add_meeting("second meeting", "at your mom's", datetime(12, 6, 9))
        self.man.add_meeting("third meeting", "Never", datetime(19, 10, 21))

        print(self.man.print_all_task())
        print(self.man.remove_task(1))
        print(self.man.remove_task(1))
        print(self.man.remove_task(1))

        print(self.man.print_all_meetings())
        print(self.man.remove_meeting(1))
        print(self.man.remove_meeting(1))
        print(self.man.remove_meeting(1))

        self.assertEqual(self.man.tasks, [])
        self.assertEqual(self.man.meetings, [])


@unittest.skip("not implemented yet")
class TestBackupNRecovery(unittest.TestCase):
    def setUp(self):
        pass

    def test_recover(self):
        pass

    def test_backup(self):
        pass

    def tesrDown(self):
        pass


if __name__ == "__main__":
    pass
