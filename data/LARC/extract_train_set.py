import os
import random
import json
import shutil

random.seed(123)
files = os.listdir('tasks_json/')
file_sample = random.sample(files, 50)
with open('arc_subset.json','r') as f:
    data = json.load(f)
cnt = 0
final_sample = []
for file in sorted(file_sample):
    with open('tasks_json/' + file, 'r') as f:
        cur_data = json.load(f)
    flag = False
    for test_data in data:
        if cur_data['name'] == test_data['name']:
            flag = True
            break
    if not flag:
        final_sample.append(file)
        cnt += 1
    if cnt == 40:
        break

os.makedirs('larc_subset/',exist_ok=True)
for file in final_sample:
    shutil.copy('tasks_json/' + file, 'larc_subset/' + file)
# json_final = []
# for i, file in enumerate(final_sample):
#     with open('training/' + file, 'r') as f:
#         cur_data = json.load(f)
#     cur = {'id': i + 1, 'name': file, "data": cur_data}
#     json_final.append(cur)

# with open('arc_subset_train.json', 'w') as f:
#     f.write('[')
#     for i in range(40):
#         f.write(json.dumps(json_final[i]))
#         if i != 39:
#             f.write(',\n')
#     f.write(']')

