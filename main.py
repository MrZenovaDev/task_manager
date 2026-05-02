# This is CLI to do task manager
# I made this as a project to build my skills in regex
# I learnt many python things by making this like
# 1.how to make a program bug free
# 2.more python functions like path, datetime

import re
import json
from pathlib import Path
from datetime import datetime

# these are the files path
task_list_file = Path("tasks.json")
deleted_tasks_file = Path("dels.json")

# these just creates the files if there isnt created in the folder and dumps an empty list
if not deleted_tasks_file.exists():
    with open("dels.json", "w") as a:
        json.dump([], a)

if not task_list_file.exists():
    with open("tasks.json", "w") as c:
        json.dump([], c)

# these opens the files and loads the tasks and deleted tasks but if that is empty then makes it empty list
with open("tasks.json", "r") as x:
    try:
        task_list = json.load(x)
    except json.JSONDecodeError:
        task_list = []

with open("dels.json", 'r') as u:
    try:
        delete_data = json.load(u)
    except json.JSONDecodeError:
        delete_data = []


# this gets the task using a regular expression thing
def get_task():
    task_data = []
    format_pattern_without_due = r"""
    (?=.*title=(.+?)\s+priority=)
    (?=.*priority=(\w+))
    """
    format_pattern_with_due = r"(?=.*due=(\d{4}/\d{2}/\d{2}))"
    print("Please enter task in this format:")
    data = {}
    user_input_try = 0
    while True:
        print("format:title=task priority=low/medium/high due=yyyy/mm/dd(optional) ")
        user_text = input("Enter task:")
        match_without_due = re.search(format_pattern_without_due, user_text, re.VERBOSE)
        match_with_due = re.search(format_pattern_with_due, user_text)
        if not match_without_due:
            print("." * 50)
            print("Please enter in the correct format!")
            print("." * 50)
            user_input_try += 1
            if user_input_try == 3:
                return 0
        else:
            if match_with_due:
                due = match_with_due.group(1)
                try:
                    datetime.strptime(due, "%Y/%m/%d")
                    data["due"] = due
                    break
                except ValueError:
                    print("****[Invalid date!Please enter again:]****")
            else:
                break
    task, priority = match_without_due.groups()
    data["title"] = task
    data["priority"] = priority.lower()
    data["completed"] = False
    task_data.append(data)
    return task_data


# lists the tasks in the tasks_list
def list_tasks(tasks_list):
    if not tasks_list:
        print("-_" * 50)
        print("There are no tasks created!")
        print("-_" * 50)
        return
    for i, task in enumerate(tasks_list, 1):
        print(f"{i}.Title:{task['title']}")
        print(f"  Priority:{task['priority']}")
        if "due" in task:
            print(f"  Due:{task['due']}")
        if task["completed"]:
            print(f"  Completed:✅")
        else:
            print(f"  Completed:❌")
        print("-" * 50)


# checks task as completed
def check(index, tasks):
    if 0 <= index < len(tasks):
        if not tasks[index]["completed"]:
            tasks[index]["completed"] = True
            return True
        else:
            print("The task is already completed!")
            return False
    else:
        print("Invalid serial number:please enter again")
        return False


# deletes task
def delete(index, tasks):
    deleted = tasks.pop(index)
    print(f"Deleted ({deleted['title']})")
    return deleted


# searches tasks based on keyword
def search(keyword, tasks):
    result = []
    for i, task in enumerate(tasks, 0):
        if keyword in task["title"].lower():
            result.append((i, task["title"]))
    return result


# prints a report
def report(tasks):
    completed = 0
    pending = 0
    total_tasks = 0
    priority_high = 0
    priority_med = 0
    priority_low = 0
    for task in tasks:
        total_tasks += 1
        if task["completed"] == True:
            completed += 1
        else:
            pending += 1
        if task["priority"] == "high":
            priority_high += 1
        elif task["priority"] == "medium":
            priority_med += 1
        else:
            priority_low += 1
    print(f"""
{"-" * 50}
completed: {completed}
pending: {pending}
total tasks: {total_tasks}
priority:
  high:{priority_high}
  medium:{priority_med}
  low:{priority_low}
{"-" * 50}
""")


# This is for listing search tasks
def list_search_tasks(index_list, task_list):
    for index in index_list:
        task = task_list[index]
        print(f"{index + 1}.Title:{task['title']}")
        print(f"  Priority:{task['priority']}")
        if "due" in task:
            print(f"  Due:{task['due']}")
        if task["completed"]:
            print(f"  Completed:✅")
        else:
            print(f"  Completed:❌")
        print("-" * 50)


# welcome
print("Welcome to tasks-lists-manager ;")

# gets correct user choice
while True:
    while True:
        try:
            # these are options
            print("""
:(options):
1.Add tasks
2.List tasks
3.Checkmark tasks
4.Search tasks
5.Delete tasks
6.Show report
7.Exit
""")
            print("_" * 50)
            # this is for making program bug free when a user inputs string
            try:
                user_choice = int(input(":"))
            except ValueError:
                print("Please enter valid option!")
                continue
            print("-" * 50)
            if 1 <= user_choice <= 7:
                break
            else:
                print("Invalid option!Please enter again")
        except ValueError:
            print("Invalid option .Please enter (1-7)!")

    # matches the choice or option
    match user_choice:
        # adds tasks into json file and prints tasks have been added
        case 1:
            new_tasks = get_task()
            if new_tasks != 0:
                task_list.extend(new_tasks)
                with open("tasks.json", "w") as As:
                    json.dump(task_list, As, indent=4)
                print("_-" * 50)
                print('Tasks have been added successfully.')
                print("_-" * 50)
            else:
                print("Option quitted")

        # this just calls the list function so it lists tasks
        case 2:
            list_tasks(task_list)

        # this lists task then checks the specific task
        case 3:
            list_tasks(task_list)
            while True:
                print("Enter the serial number of the task that you want to check:")
                try:
                    SN = int(input(":="))
                except ValueError:
                    print("Invalid input!")
                    continue
                if 1 <= SN <= len(task_list):
                    tasks = check(SN - 1, task_list)
                    if tasks == True:
                        with open("tasks.json", "w") as checked:
                            json.dump(task_list, checked, indent=4)
                        print("**CHECKED!**")
                        break
                else:
                    print("~" * 50)
                    print("Please enter serial number within the range:")
                    print("~" * 50)

        # this is for searching based on the keyword. It searches the task_list
        case 4:
            keyword = input("Enter keyword for searching: ").lower()
            search_result = search(keyword, task_list)
            if search_result:
                index_list = []
                for result in search_result:
                    index_of_result = result[0]
                    index_list.append(index_of_result)
                list_search_tasks(index_list, task_list)
            else:
                print("NO tasks found!")

        # this lists tasks and deletes the specific task and also adds the tasks to the dels.json file
        case 5:
            list_tasks(task_list)
            print("Enter Serial number of the task you want to delete!")
            try:
                delete_index = int(input(": ")) - 1
            except:
                print("Invalid input!")
                continue
            deleted_task = delete(delete_index, task_list)
            delete_data.append(deleted_task)
            with open("dels.json", "w") as c:
                json.dump(delete_data, c, indent=4)
            print("Task have been deleted sucessfully.")

        # this makes a plain report
        case 6:
            report(task_list)

        # this breaks the loop if user wants
        case 7:
            print("Be sure to complete those tasks in time!")
            break







