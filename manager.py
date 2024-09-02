from datetime import datetime, date, timedelta
from asyncio import sleep
import sqlite3


class Meeting:
    """
    Meeting class holds all imporant information needed for hosting meetings

    Attr
    ----
    desc: simple description of meeting
    locat: location of meeting
    datetime: date and time of meeting
    ----
    """

    def __init__(self, desc: str, locat: str, datetime: datetime):
        self.desc = desc
        self.locat = locat
        self.datetime = datetime

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return f"{self.desc};{self.locat};{self.datetime.isoformat()}"

    def __str__(self):
        return f"Meeting: {self.desc} at {self.locat} at the time {self.datetime.strftime("%a %d %b, %I:%M%p")}"


class Task:
    """
    Task class holds all info needed for managing task

    Attr
    -----
    c_date: creation date of task
    d_date: due date of task
    a_date: date task was assigned to a team member
    assi_to: who task is assigned to
    -----
    """

    def __init__(self, desc: str, d_date: date, a_date: date, assi_to: str | None):
        self.desc = desc
        self.c_date = datetime.today()
        self.d_date = d_date
        self.a_date = a_date
        self.assi_to = assi_to

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return f"{self.desc};{self.c_date.isoformat()};{self.d_date.isoformat()};{self.a_date.isoformat()};{self.assi_to}"

    def __str__(self):
        task = f"Task: {self.desc} due on {self.d_date.strftime("%a %d %b")}"
        if self.assi_to is not None:
            task += f"assigned to {self.assi_to} on {self.a_date.strftime("%a %d %b")}"
        return task

    def assign_task(self, member: str):
        self.assi_to = member
        self.a_date = datetime.today()


class Manager:
    """
    Manager controls the task and meeting structures and holds multiple instances of both

    Attr
    ----
    tasks: list of task
    meetings: list of meetings
    backup_time: time until backup is required
    reminder_time: time before a reminder is issued
    """

    def __init__(self, backup: int, reminder: int):
        self.tasks = []
        self.meetings = []
        self.backup_delta = timedelta(minutes=backup)
        self.reminder_delta = timedelta(minutes=reminder)
        self.backup_db = sqlite3.connect("manager.db")

    def add_task(self, desc: str, due: date, assigned: date, assigned_to=None):
        self.tasks.append(Task(desc, due, assigned, assigned_to))

    def add_meeting(self, desc: str, locat: str, datetime: datetime):
        self.meetings.append(Meeting(desc, locat, datetime))

    def assign_task(self, task_num: int, member: str):
        self.tasks[task_num].assigned_to(member)

    def fetch_backup(self):
        pass

    def change_backup_time(
        self,
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0,
    ):
        self.backup_delta = timedelta(
            days, seconds, microseconds, milliseconds, minutes, hours, weeks
        )

        return "Backup frequency changed to {} seconds".format(
            self.backup_delta.total_seconds()
        )

    def change_reminder_time(
        self,
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0,
    ):
        self.reminder_delta = timedelta(
            days, seconds, microseconds, milliseconds, minutes, hours, weeks
        )

        return "Reminder frequency changed to {} seconds".format(
            self.reminder_delta.total_seconds()
        )

    # NOTE:database must be created
    def backup(self):
        # backup to db
        self.backup_db.executemany("INSERT INTO tasks VALUES ?", self.tasks)
        self.backup_db.executemany("INSERT INTO meetings VALUES ?", self.meetings)

    def print_all_task(self):
        counter = 1
        task_list = ""
        for task in self.tasks:
            task_list += f"{counter}: {str(task)} +\n "
        return task_list

    def print_all_meetings(self):
        counter = 1
        meeting_list = ""
        for meeting in self.meetings:
            meeting_list += f"{counter}: {str(meeting)} +\n "
        return meeting_list

    ########## async task ############
    async def backup_trigger(self):
        backup_time = datetime.today() + self.backup_delta
        while True:
            # if time to backup, backup. Else wait until time
            if backup_time <= datetime.today():
                # Blocking
                print("Backing up data")
                self.backup()
                print("Data backed up")
                # set next backup time
                backup_time = datetime.today() + self.backup_delta
            else:
                wakeup_time = datetime.today() - backup_time
                await sleep(wakeup_time.total_seconds())

    async def remind_todo_trigger(self):
        reminder_time = datetime.today() + self.reminder_delta
        while True:
            for task in self.tasks:
                # if time to remind, remind.
                if reminder_time <= task.d_date:
                    # remind user of task
                    print(task)
                    # set next reminder time
                    reminder_time = datetime.today() + self.reminder_delta

            wakeup_time = datetime.today() - reminder_time
            await sleep(wakeup_time.total_seconds())

    async def remind_meeting_trigger(self):
        reminder_time = datetime.today() + self.reminder_delta
        while True:
            for meeting in self.meetings:
                # if time to remind, remind.
                if reminder_time <= meeting.datetime:
                    # remind user of meeting
                    print(meeting)
                    # set next reminder time
                    reminder_time = datetime.today() + self.reminder_delta

            wakeup_time = datetime.today() - reminder_time
            await sleep(wakeup_time.total_seconds())

    # TODO: make triggers for that take in context as a argument
