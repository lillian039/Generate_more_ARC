import json
import os

file_list = os.listdir('code_and_requirement_complete/')

with open('arc_subset.json', 'r') as f:
    test_daa = json.load(f)
data_wo_test = []

for file in file_list:
    with open(f'code_and_requirement_complete/{file}', 'r') as f:
        data = json.load(f)
    flag = False
    if data['generalizable'] == False:
        continue
    for item in test_daa:
        if item['name'] == data['name']:
            flag = True
            break
    if flag:
        continue
    data_train = []
    for i, train_example in enumerate(data['train_io']['inputs']):
        data_train.append({
            'input': train_example,
            'output': data['train_io']['outputs'][i]
        })
    data_test = [{
        'input': data['test_io']['inputs'][0],
        'output': data['test_io']['outputs'][0]
    }]
    data_wo_test.append({
        'name': data['name'],
        'data': {
            'train': data_train,
            'test': data_test
        },
        'code': data['python'].replace('main(','transform_grid(')
    })

with open('arc_train_wo_test_code.json', 'w') as f:
    f.write('[\n')
    for i, task in enumerate(data_wo_test):
        json.dump(task, f)
        if i == len(data_wo_test) - 1:
            f.write('\n]')
        else:
            f.write(',\n')

    