from decimal import Decimal


def trim(title, length):
    if (len(title) <= length):
        task_name = title[0:length]
    else:
        task_name = title[0:length-3] + "..."

    task_length = len(task_name)
    if (task_length <= length):
        task_name += ' ' * (length - task_length)

    return task_name


def print_task(task):
    TASK_NAME_LENGTH = 50
    result = dict()
    result['task_name'] = trim(task['title'], TASK_NAME_LENGTH)

    if Decimal(task['size']) != 0:
        result['progress'] = Decimal(task['additional']['transfer']['size_downloaded']) / Decimal(task['size']) * 100
    else:
        result['progress'] = 0

    result['status'] = task['status']
    result['speed'] = Decimal(task['additional']['transfer']['speed_download']) / 1000 / 1000
    print('{task_name}\t{status}\t{speed:0.2f}MB/s\t{progress:0.2f}%'.format(**result))


def print_tasks(tasks):
    for task in tasks:
        try:
            print_task(task)
        except Exception as e:
            print(e.message)
