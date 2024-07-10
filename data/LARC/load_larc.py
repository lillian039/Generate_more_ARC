import os
import json

def transform_list_to_str(task_list):
    task_list = task_list.replace("], [", "]\n[")
    task_list = task_list.replace(", ", " ")
    return task_list

def transfrom_example_question_code(task_train):
    str_format = ""
    for i, pair in enumerate(task_train):
        str_format += f"Example {i}:\n"
        input_str = transform_list_to_str(str(pair['input']))
        output_str = transform_list_to_str(str(pair['output']))
        str_format += f"Input:\n{input_str}\nOutput:\n{output_str}\n"
    return str_format

path = 'tasks_json/'
with open(path + '1.json', 'r') as f:
    tasks = json.load(f)

def random_eight_examples():
    path = 'larc_subset/'
    files = os.listdir(path)
    files = sorted(files)
    os.makedirs('larc_subset_eight', exist_ok=True)

    for i in range(8):
        cur_task_name = files[i]
        with open(path + cur_task_name, 'r') as f:
            task = json.load(f)
        task_train = task['train']
        str_task_train = task['name'] + '\n\n'
        str_task_train += transfrom_example_question_code(task_train) + '\n'

        for key in task['descriptions'].keys():
            task_item = task['descriptions'][key]
            if not task_item['succeeded_verification']:
                continue
            if task_item['confidence'] < 8:
                continue
            see_object = task_item['see_description']
            grid_size = task_item['grid_description']
            discription = task_item['do_description']

            str_task_train += '='*10 + 'Human Description' + '='*10 + '\n\n'
            str_task_train += see_object.replace('...', ': ') + '\n\n'
            str_task_train += grid_size.replace('...', ': ') + '\n\n'
            str_task_train += discription.replace('...', ': ') + '\n\n'

        name = cur_task_name.split('.')[0]
        with open(f'larc_subset_eight/{name}.txt', 'w') as f:
            f.write(str_task_train)

random_eight_examples()
            

# print(tasks.keys()) 
#   ['descriptions', 'name', 'test', 'train']
# print(tasks['descriptions'].keys())
#   ['2def69cd-2840-41b2-8964-e4c2e11b4b78', '6206e6be-8f69-4c1b-b8c0-65aae0dc7659', 'bb575924-670b-4351-bbe9-9cdbd1d91c2c', 'cd346d97-ec6f-41ca-9389-23939676c3dd']
# tasks['descriptions'][key]
#   ['action_sequence', 'attempt_jsons', 'builds', 'confidence', 'description_time', 
#   'do_description', 'grid_description', 'max_idle_time', 'num_verification_attempts', 
#   'see_description', 'succeeded_verification', 'timestamp', 'uid', 'verification_time']
# print(tasks['name'])
# for key in tasks['descriptions']:
#     print(key, tasks['descriptions'][key]['do_description'], tasks['descriptions'][key]['confidence'], tasks['descriptions'][key]['succeeded_verification'])
#     print(tasks['descriptions'][key]['grid_description'])
#     print(tasks['descriptions'][key]['see_description'])
#     print(tasks['descriptions'][key]['num_verification_attempts'])
#     print(tasks['descriptions'][key]['timestamp'])