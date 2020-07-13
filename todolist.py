from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Menu:

    def __init__(self):
        self.action = True
        self.dict = {}

    def start(self):
        while self.action:
            print("1) Today's tasks")
            print("2) Week's tasks")
            print("3) All tasks")
            print("4) Missed tasks")
            print("5) Add task")
            print("6) Delete task")
            print("0) Exit")
            inp = input()
            if inp == "1":
                self.check_today()
            if inp == "2":
                self.week_task()
            if inp == "3":
                self.all_tasks()
            if inp == "4":
                self.missed_tasks()
            if inp == "5":
                self.add_task()
            if inp == "6":
                self.delete_task()
            if inp == "0":
                self.action = False
                print("Bye!")

    def check_today(self):
        print()
        today = datetime.today().date()
        rows = session.query(Table).filter(Table.deadline == today).all()
        print(f"Today {today.strftime('%d %b')}:")
        number = 1
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for i in range(len(rows)):
                print(f"{number}. {rows[i].task}")
                number += 1
        print()

    def week_task(self):
        today = datetime.today().date()

        in_a_week = today + timedelta(days=7)
        in_a_week = in_a_week.strftime("%A %d %b")
        current_day = today.strftime("%A %d %b")
        while current_day != in_a_week:
            print()
            print(f"{current_day}:")
            number = 1
            rows = session.query(Table).filter(Table.deadline == today).all()
            if len(rows) > 0:
                for el in rows:
                    date = el.deadline.strftime("%A %d %b")
                    if date == current_day:
                        print(f"{number}. {el.task}")
                        number += 1
            else:
                print("Nothing to do!")
            today += timedelta(days=1)
            current_day = today.strftime("%A %d %b")
        print()

    def all_tasks(self):
        rows = session.query(Table).all()
        sorted_rows = []
        for i in rows:
            elem = i.deadline, i.task
            sorted_rows.append(elem)
        sorted_rows.sort()
        number = 1
        for task in sorted_rows:
            date = task[0].strftime("%d %b")
            print(f"{number}. {task[1]}. {date}")
            number += 1
        print()

    def missed_tasks(self):
        today = datetime.today().date()
        rows = session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
        number = 1
        print("Missed tasks:")
        for elem in rows:
            date = elem.deadline.strftime("%d %b")
            print(f"{number}. {elem.task}. {date}")
            number += 1
        print()

    def add_task(self):
        print("Enter task")
        inp_task = input()
        print("Enter deadline")
        inp_d = input().split("-")
        inp_deadline = datetime(int(inp_d[0]), int(inp_d[1]), int(inp_d[2]))
        new_row = Table(task=f'{inp_task}',
                        deadline=inp_deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
        print()

    def delete_task(self):
        rows = session.query(Table).order_by(Table.deadline).all()
        number = 1
        if len(rows) > 0:
            print("Chose the number of the task you want to delete:")
            for elem in rows:
                date = elem.deadline.strftime("%d %b")
                print(f"{number}. {elem.task}. {date}")
                self.dict[str(number)] = elem.task
                number += 1
        else:
            print("Nothing to delete")

        number_delete = input()
        if number_delete in self.dict:
            to_kick = self.dict[number_delete]
            session.query(Table).filter(Table.task == to_kick).delete()
            session.commit()
            print("The task has been deleted!")
            self.dict = {}
        else:
            print("incorrect number")
        print()





menu = Menu()
menu.start()

