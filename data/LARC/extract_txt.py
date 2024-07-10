import json
import os

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

path_train_arc = 'arc_subset_train.json'
with open(path_train_arc, 'r') as f:
    data = json.load(f)

os.makedirs('arc_subset_train_example/', exist_ok=True)
for data_item in data:
    task_train = data_item['data']['train']
    str_task_train = transfrom_example_question_code(task_train)
    task_name = data_item['name'].split('.')[0]
    with open(f'arc_subset_train_example/{task_name}.txt', 'w') as f:
        f.write(str_task_train)
        

