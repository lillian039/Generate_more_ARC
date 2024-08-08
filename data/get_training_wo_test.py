import json
import os

file_list = os.listdir('training/')

with open('arc_subset.json', 'r') as f:
    test_daa = json.load(f)
data_wo_test = []
for file in file_list:
    flag = False
    for item in test_daa:
        if item['name'] == file:
            flag = True
            break
    if flag:
        continue

    with open(f'training/{file}', 'r') as f:
        data = json.load(f)
    data_wo_test.append({
        'name': file,
        'data': data
    })

with open('arc_train_wo_test.json', 'w') as f:
    f.write('[\n')
    for i, task in enumerate(data_wo_test):
        json.dump(task, f)
        if i == len(data_wo_test) - 1:
            f.write('\n]')
        else:
            f.write(',\n')

    