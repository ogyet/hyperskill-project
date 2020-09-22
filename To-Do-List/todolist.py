# Write your code here
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import sys

Base = declarative_base()
today = datetime.today().date()

class Task(Base):
    __tablename__ = 'task'
    id = Column('id', Integer, primary_key=True)
    task = Column('task', String, default='New Task')
    deadline = Column('deadline', Date, default=today)


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def update_task(function):
    global session
    if function == "add":
        task_input = input('Enter task\n')
        task_deadline = datetime.strptime(input('Enter deadline\n'),'%Y-%m-%d')
        new_row = Task(task=task_input, deadline=task_deadline)
        session.add(new_row)
        session.commit()
        print('The task has been added!')
    elif function == "delete":
        tasks = session.query(Task).order_by(Task.deadline).all()
        print("Choose the number of the task you want to delete:")
        counter = 1
        for task in tasks:
            task_print = "{}. {}.".format(counter, task.task)
            print(task_print, datetime.strftime(task.deadline, '%d %b'))
            counter += 1
        choice = int(input())-1
        session.delete(tasks[choice])
        session.commit()
        print("The task has been deleted!")

def show_tasks(period=datetime(9999, 1, 1).date()):
    global session, today
    if datetime(9999, 1, 1).date() > period >= today:
        tasks = session.query(Task).filter(Task.deadline.between(today, period)).order_by(Task.deadline).all()
        days = (period-today).days + 1
        today_counter = today
        if days == 1:
            print('\nToday ', datetime.strftime(today, '%d %b'), ':', sep='')
        else:
            print('\n', datetime.strftime(today_counter, '%A %d %b'), ':', sep='')
        for i in range(days):
            counter = 1
            if len(tasks) > 0:
                for task in tasks:
                    task_print = "{}. {}".format(counter, task.task)
                    print(task_print)
                    counter += 1
            else:
                print('Nothing to do!')
            if period <= today_counter:
                continue
            today_counter += timedelta(days=1)
            print('\n', datetime.strftime(today_counter, '%A %d %b'), ':', sep='')
    else:
        if datetime(9999, 1, 1).date() == period:
            tasks = session.query(Task).order_by(Task.deadline).all()
            print("All tasks:")
        else:
            tasks = session.query(Task).filter(Task.deadline < today).order_by(Task.deadline).all()
            print("Missed tasks:")
            if len(tasks) == 0:
                print("Nothing is missed!")
        counter = 1
        for task in tasks:
            task_print = "{}. {}.".format(counter, task.task)
            print(task_print, datetime.strftime(task.deadline, '%d %b'))
            counter += 1

if __name__ == '__main__':
    while(True):
        try:
            choice = int(input("\n1) Today\'s tasks\n2) Week\'s tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n"))
            if choice in (1, 2, 3,4):
                if choice == 3:
                    show_tasks()
                    continue
                time_period = today
                if choice == 2:
                    time_period += timedelta(days=6)
                if choice == 4:
                    time_period -= timedelta(days=1)
                show_tasks(time_period)
            elif choice == 5:
                update_task("add")
            elif choice == 6:
                update_task("delete")
            elif choice == 0:
                print('Bye!')
                session.close()
                sys.exit(0)
            else:
                raise ValueError('{} is an invalid input')
        except ValueError:
            print('Invalid Input')
