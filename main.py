import re

def add_tasks():
    task_data=[]
    format_pattern_without_due=r"""
(?=.*title=(\w+))
(?=.*priority=(\w+))
""" 
    format_pattern_with_due=r"(?=.*due=(\d{4}/\d{2}/\d{2}))"
    print("Please enter task in this format:")
    while True:
        print("format:title=task priority=low/medium/high due=yyyy/mm/dd(optional) ")
        user_text=input("Enter task:")
        match_without_due=re.search(format_pattern_without_due,user_text,re.VERBOSE)
        if match_without_due:
            data={}
            task,priority=match_without_due.groups()
            data["task"]=task
            data["priority"]=priority
            match_with_due=re.search(format_pattern_with_due,user_text)
            if match_with_due:
                due=match_with_due.group(1)
                data["due"]=due
            task_data.append(data)
            break
        else:
            print("Please enter data in the correct pattern as shown:")
    return task_data

def list_tasks(tasks_list):
    for i,task in enumerate(tasks_list,1):
        print(f"{i}.Title:{task["title"]}")
        print(f"  Priority:{task["priority"]}")
        if "due" in task:
            print(f"  Due:{task["due"]}")
        if "completed" in task:
            if task["completed"]:
                print(f"  Completed:✅")
            else:
                print(f"  Completed:❌")
list_tasks([{"title":"do","priority":"high"}])
        







