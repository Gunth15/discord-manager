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

    #    def __conform__(self, protocol):
    #        if protocol is sqlite3.PrepareProtocol:
    #            return (self.desc, self.locat, self.datetime.isoformat())

    def __str__(self):
        return f"Meeting: {self.desc} at {self.locat} at the time {self.datetime.strftime("%a %d %b, %I:%M%p")} "

    def to_tuple(self):
        return (self.desc, self.locat, self.datetime.isoformat())


class Task:
    """
    Task class holds all info needed for managing task

    Attr
    -----
    c_date: creation date of task
    d_date: due date of task
    a_date: date task was assigned to team
    assi_to: who task is assigned to
    -----
    """

    def __init__(
        self,
        desc: str,
        d_date: date,
        a_date: date,
        assi_to: str | None,
        c_date=date.today(),
    ):
        self.desc = desc
        self.c_date = c_date
        self.d_date = d_date
        self.a_date = a_date
        self.assi_to = assi_to

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return (
                self.desc,
                self.c_date.isoformat(),
                self.d_date.isoformat(),
                self.a_date.isoformat(),
                self.assi_to,
            )

    def __str__(self):
        # TODO: Need to handle case whre due date is none
        task = f"Task: {self.desc} due on {self.d_date.strftime("%a %d %b")} and was assigned on {self.a_date.strftime("%a %d %b")} "
        if self.assi_to is not None:
            task += f" and was assigned to {self.assi_to} "
        return task

    def assign_task(self, member: str):
        self.assi_to = member

    def to_tuple(self):
        return (
            self.desc,
            self.c_date.isoformat(),
            self.d_date.isoformat(),
            self.a_date.isoformat(),
            self.assi_to,
        )


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
        self.backup_db = sqlite3.connect(
            "manager.db", detect_types=sqlite3.PARSE_COLNAMES
        )

    def add_task(
        self, desc: str, due: date, assigned: date, assigned_to: str | None = None
    ):
        self.tasks.append(Task(desc, due, assigned, assigned_to))

    def add_meeting(self, desc: str, locat: str, datetime: datetime):
        self.meetings.append(Meeting(desc, locat, datetime))

    def assign_task(self, task_num: int, member: str):
        self.tasks[task_num - 1].assign_task(member)

    def remove_task(self, task_num: int) -> str:
        task_num = task_num - 1
        if task_num <= 0 or task_num >= len(self.tasks):
            del_task = "nothing"
        else:
            del_task = self.tasks.pop(task_num)
        return f"{del_task} was deleted "

    def remove_meeting(self, meeting_num: int) -> str:
        meeting_num = meeting_num - 1
        if meeting_num < 0 or meeting_num >= len(self.meetings):
            del_meeting = "nothing"
        else:
            del_meeting = self.meetings.pop(meeting_num - 1)
        return f"{del_meeting} was deleted "

    def print_all_task(self) -> str:
        counter = 1
        task_list = ""

        if self.tasks == []:
            return "No task..."

        for task in self.tasks:
            task_list += f"{counter}: {str(task)} \n"
            counter += 1
        return task_list

    def print_all_meetings(self) -> str:
        counter = 1
        meeting_list = ""
        if self.meetings == []:
            return "No meetings..."

        for meeting in self.meetings:
            meeting_list += f"{counter}: {str(meeting)} \n"
            counter += 1
        return meeting_list

    # NOTE:database must be created

    ########## sqlite3 backup related methods #########
    # TODO: Make method to clear db cache
    def recover(self):
        print("Recovering data")
        self.meetings = self.backup_db.execute("SELECT * FROM meetings").fetchall()
        self.tasks = self.backup_db.execute("SELECT * FROM tasks").fetchall()
        print("Successfully recovered backup!!! ")

    def backup(self):
        # backup to db
        print("Backing up")
        self.backup_db.executemany(
            "INSERT INTO tasks (desc,c_date,d_date,a_date,assi_to) VALUES (?,?,?,?,?)",
            list(map(lambda task: task.to_tuple(), self.tasks)),
        )
        self.backup_db.executemany(
            "INSERT INTO meetings (desc, locat, datetime) VALUES (?,?,?)",
            list(map(lambda meeting: meeting.to_tuple(), self.meetings)),
        )
        print("Successfully backed up!!! ")

    def change_backup_time(
        self,
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0,
    ) -> str:
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
    ) -> str:
        self.reminder_delta = timedelta(
            days, seconds, microseconds, milliseconds, minutes, hours, weeks
        )

        return "Reminder frequency changed to {} seconds".format(
            self.reminder_delta.total_seconds()
        )

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


# sqlite3 converters
def convert_meetings(meeting):
    desc, locat, date_time, _ = meeting
    return Meeting(desc, locat, datetime.fromisoformat(date_time))


def convert_tasks(task):
    desc, c_date, d_date, a_date, assi_to, _ = task
    return Task(
        desc,
        date.fromisoformat(d_date),
        date.fromisoformat(a_date),
        assi_to,
        c_date=date.fromisoformat(c_date),
    )
